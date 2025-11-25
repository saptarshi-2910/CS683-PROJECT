# define SIZE_1X
# if defined(SIZE_1X)
// MICRO Size
# define HISTORY_TABLE_SET            (8)
# define HISTORY_TABLE_WAY            (16)
# define TABLE_SET_MASK               (0x7)
# define BERTI_TABLE_SIZE             (16)
# define BERTI_TABLE_STRIDE_SIZE      (16)

// Cross-IP Delta Graph parameters
# define GLOBAL_DELTA_TABLE_SIZE      (256)
# define GLOBAL_DELTA_HASH_MASK       (0xFF)
# define MAX_IP_CORRELATION           (4)

// Phase detection parameters
# define NUM_PHASES                   (4)
# define PHASE_DETECTION_INTERVAL     (10000)
# define PHASE_SIGNATURE_SIZE         (8)

# elif defined(SIZE_2X)
// 2xMICRO Size
# define HISTORY_TABLE_SET            (16)
# define HISTORY_TABLE_WAY            (32)
# define TABLE_SET_MASK               (0xF)
# define BERTI_TABLE_SIZE             (32)
# define BERTI_TABLE_STRIDE_SIZE      (32)

# define GLOBAL_DELTA_TABLE_SIZE      (512)
# define GLOBAL_DELTA_HASH_MASK       (0x1FF)
# define MAX_IP_CORRELATION           (8)

# define NUM_PHASES                   (8)
# define PHASE_DETECTION_INTERVAL     (10000)
# define PHASE_SIGNATURE_SIZE         (16)

# elif defined(SIZE_4X)
// 4xMICRO Size
# define HISTORY_TABLE_SET            (32)
# define HISTORY_TABLE_WAY            (64)
# define TABLE_SET_MASK               (0x1F)
# define BERTI_TABLE_SIZE             (64)
# define BERTI_TABLE_STRIDE_SIZE      (64)

# define GLOBAL_DELTA_TABLE_SIZE      (1024)
# define GLOBAL_DELTA_HASH_MASK       (0x3FF)
# define MAX_IP_CORRELATION           (16)

# define NUM_PHASES                   (16)
# define PHASE_DETECTION_INTERVAL     (10000)
# define PHASE_SIGNATURE_SIZE         (32)

# elif defined(SIZE_050X)
// 0.5xMICRO Size
# define HISTORY_TABLE_SET            (4)
# define HISTORY_TABLE_WAY            (8)
# define TABLE_SET_MASK               (0x3)
# define BERTI_TABLE_SIZE             (8)
# define BERTI_TABLE_STRIDE_SIZE      (8)

# define GLOBAL_DELTA_TABLE_SIZE      (128)
# define GLOBAL_DELTA_HASH_MASK       (0x7F)
# define MAX_IP_CORRELATION           (2)

# define NUM_PHASES                   (2)
# define PHASE_DETECTION_INTERVAL     (10000)
# define PHASE_SIGNATURE_SIZE         (4)

# elif defined(SIZE_025X)
// 0.25xMICRO Size
# define HISTORY_TABLE_SET            (2)
# define HISTORY_TABLE_WAY            (4)
# define TABLE_SET_MASK               (0x1)
# define BERTI_TABLE_SIZE             (4)
# define BERTI_TABLE_STRIDE_SIZE      (4)

# define GLOBAL_DELTA_TABLE_SIZE      (64)
# define GLOBAL_DELTA_HASH_MASK       (0x3F)
# define MAX_IP_CORRELATION           (2)

# define NUM_PHASES                   (2)
# define PHASE_DETECTION_INTERVAL     (10000)
# define PHASE_SIGNATURE_SIZE         (2)

#endif