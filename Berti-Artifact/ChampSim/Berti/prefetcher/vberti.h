#ifndef VBERTI_H_
#define VBERTI_H_

#include "vberti_size.h"
#include "cache.h"
#include <algorithm>
#include <vector>
#include <tuple>
#include <queue>
#include <cmath>
#include <map>
#include <unordered_map>
#include <set>
#include <stdlib.h>
#include <time.h>

// vBerti defines
# define LATENCY_TABLE_SIZE           (L1D_MSHR_SIZE + 16)

// Mask
# define MAX_HISTORY_IP               (8)
# define MAX_PF                       (16)
# define MAX_PF_LAUNCH                (12)
# define STRIDE_MASK                  (12)

// Mask
# define IP_MASK                      (0x3FF)
# define TIME_MASK                    (0xFFFF)
# define LAT_MASK                     (0xFFF)
# define ADDR_MASK                    (0xFFFFFF)

// AGGRESSIVE: Much lower confidence thresholds for server workloads
# define CONFIDENCE_MAX               (12)      // Reduced from 16
# define CONFIDENCE_INC               (2)       // Increased from 1
# define CONFIDENCE_INIT              (3)       // Increased from 1
# define CONFIDENCE_L1                (45)      // Reduced from 65
# define CONFIDENCE_L2                (30)      // Reduced from 50
# define CONFIDENCE_L2R               (18)      // Reduced from 35
# define MSHR_LIMIT                   (80)      // Increased from 70

// Stride rpl
# define R                            (0x0)
# define L1                           (0x1)
# define L2                           (0x2)
# define L2R                          (0x3)

// AGGRESSIVE: Cross-IP correlation - lower thresholds
# define GLOBAL_DELTA_CONFIDENCE_THRESHOLD  (3)   // Reduced from 8
# define CORRELATION_STRENGTH_THRESHOLD     (2)   // Reduced from 5
# define MIN_IP_CONFIDENCE_FOR_CORRELATION  (2)   // Reduced from 4

// AGGRESSIVE: Phase detection - more sensitive
# define PHASE_SIMILARITY_THRESHOLD   (40)   // Reduced from 60
# define PHASE_MISS_RATE_THRESHOLD    (8)    // Reduced from 12

// Structs
typedef struct latency_table {
    uint64_t addr;
    uint64_t tag;
    uint64_t time;
    uint8_t  pf;
} latency_table_t;

typedef struct history_table {
    uint64_t tag;
    uint64_t addr;
    uint64_t time;
} history_table_t;

typedef struct Stride {
    uint64_t conf;
    int64_t stride;
    uint8_t rpl;
    float   per;
    uint64_t last_used;
    uint8_t from_correlation;  // NEW: Track if from correlation
    Stride(): conf(0), stride(0), rpl(0), per(0), last_used(0), from_correlation(0) {};
} stride_t; 

typedef struct VBerti {
    stride_t *stride;
    uint64_t conf;
    uint64_t total_used;
    uint8_t phase_id;
    uint8_t needs_help;
    uint64_t last_access;      // NEW: Track recency
    uint16_t access_count;     // NEW: Track frequency
} vberti_t;

typedef struct shadow_cache {
    uint64_t addr;
    uint64_t lat;
    uint8_t  pf;
} shadow_cache_t;

// Global Delta Entry - Enhanced
typedef struct GlobalDeltaEntry {
    int64_t delta;
    uint16_t confidence;
    uint8_t ip_count;
    uint64_t last_seen;
    std::set<uint64_t> contributing_ips;  // NEW: Track which IPs use this
    
    GlobalDeltaEntry(): delta(0), confidence(0), ip_count(0), last_seen(0) {}
} global_delta_entry_t;

typedef struct IPCorrelation {
    uint64_t ip;
    uint8_t strength;
    int64_t common_delta;
    
    IPCorrelation(): ip(0), strength(0), common_delta(0) {}
} ip_correlation_t;

// Phase detection - Enhanced
typedef struct PhaseSignature {
    uint32_t miss_rate;
    uint64_t sample_count;
    uint64_t last_update;
    std::vector<int64_t> dominant_deltas;  // NEW: Track common deltas per phase
    
    PhaseSignature(): miss_rate(0), sample_count(0), last_update(0) {}
} phase_signature_t;

typedef struct PhaseInfo {
    uint8_t current_phase;
    uint8_t prev_phase;        // NEW: Track previous phase
    uint64_t last_phase_check;
    uint64_t phase_transition_count;
    uint64_t sample_misses;
    uint64_t sample_accesses;
    phase_signature_t signatures[NUM_PHASES];
    
    PhaseInfo(): current_phase(0), prev_phase(0), last_phase_check(0), 
                 phase_transition_count(0), sample_misses(0), sample_accesses(0) {}
} phase_info_t;

// Existing structs
latency_table_t latencyt[NUM_CPUS][LATENCY_TABLE_SIZE];
history_table_t historyt[NUM_CPUS][HISTORY_TABLE_SET][HISTORY_TABLE_WAY];
shadow_cache_t scache[NUM_CPUS][L1D_SET][L1D_WAY];
std::map<uint64_t, vberti_t*> vbertit[NUM_CPUS];
std::queue<uint64_t> vbertit_queue[NUM_CPUS];
history_table_t *history_pointers[NUM_CPUS][HISTORY_TABLE_SET];

// Global Delta Graph
std::unordered_map<int64_t, global_delta_entry_t> global_delta_graph[NUM_CPUS];
std::unordered_map<uint64_t, std::vector<ip_correlation_t>> ip_correlation_map[NUM_CPUS];

// Phase detection
phase_info_t phase_info[NUM_CPUS];
std::map<uint64_t, std::map<uint8_t, vberti_t*>> phase_vbertit[NUM_CPUS];

void notify_prefetch(uint64_t addr, uint64_t cycle);

// Auxiliary latency table functions
void latency_table_init(uint32_t cpu);
uint8_t latency_table_add(uint64_t line_addr, uint64_t tag, uint32_t cpu, uint8_t pf);
uint8_t latency_table_add(uint64_t line_addr, uint64_t tag, uint32_t cpu, uint8_t pf, uint64_t cycle);
uint64_t latency_table_del(uint64_t line_addr, uint32_t cpu);
uint64_t latency_table_get_ip(uint64_t line_addr, uint32_t cpu);
uint64_t latency_table_get(uint64_t line_addr, uint32_t cpu);

// Shadow cache functions
void shadow_cache_init(uint32_t cpu);
uint8_t shadow_cache_add(uint32_t cpu, uint32_t set, uint32_t way, uint64_t line_addr, uint8_t pf, uint64_t latency);
uint8_t shadow_cache_get(uint32_t cpu, uint64_t line_addr);
uint8_t shadow_cache_pf(uint32_t cpu, uint64_t line_addr);
uint8_t shadow_cache_is_pf(uint32_t cpu, uint64_t line_addr);
uint8_t shadow_cache_latency(uint32_t cpu, uint64_t line_addr);

// Auxiliar history table functions
void history_table_init(uint32_t cpu);
void history_table_add(uint64_t tag, uint32_t cpu, uint64_t addr);
uint16_t history_table_get(uint32_t cpu, uint32_t latency, uint64_t tag, uint64_t act_addr, 
                           uint64_t ip[HISTORY_TABLE_WAY], uint64_t addr[HISTORY_TABLE_WAY], uint64_t cycle);

// Auxiliar vberti table functions
void vberti_table_add(uint64_t tag, uint32_t cpu, int64_t stride);
uint8_t vberti_table_get(uint64_t tag, uint32_t cpu, stride_t res[MAX_PF]);
void vberti_increase_conf_ip(uint64_t tag, uint32_t cpu);

void find_and_update(uint32_t cpu, uint64_t latency, uint64_t tag, uint64_t cycle, uint64_t line_addr);

// AGGRESSIVE: Global Delta Graph functions
void global_delta_init(uint32_t cpu);
void global_delta_add_aggressive(uint32_t cpu, int64_t delta, uint64_t ip);
std::vector<int64_t> global_delta_get_correlated_aggressive(uint32_t cpu, uint64_t ip);

// AGGRESSIVE: Phase detection functions
void phase_detection_init(uint32_t cpu);
void phase_signature_update_aggressive(uint32_t cpu, bool is_miss);
uint8_t phase_detect_aggressive(uint32_t cpu);
void phase_vberti_add_aggressive(uint64_t tag, uint32_t cpu, int64_t stride, uint8_t phase);
uint8_t phase_vberti_get_aggressive(uint64_t tag, uint32_t cpu, uint8_t phase, stride_t res[MAX_PF]);

#endif