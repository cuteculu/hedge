/*
 Navicat Premium Data Transfer

 Source Server         : MySQL
 Source Server Type    : MySQL
 Source Server Version : 50724
 Source Host           : localhost:3306
 Source Schema         : odds

 Target Server Type    : MySQL
 Target Server Version : 50724
 File Encoding         : 65001

 Date: 26/11/2019 23:05:36
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for dealer_rate
-- ----------------------------
DROP TABLE IF EXISTS `dealer_rate`;
CREATE TABLE `dealer_rate`
(
    `id`     int(10) UNSIGNED                                   NOT NULL AUTO_INCREMENT,
    `dealer` char(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL,
    `rate`   float(5, 2) UNSIGNED                               NOT NULL DEFAULT 0.00,
    PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB
  AUTO_INCREMENT = 1
  CHARACTER SET = utf8mb4
  COLLATE = utf8mb4_bin
  ROW_FORMAT = Dynamic;

INSERT INTO `dealer_rate`
VALUES (1, '竞彩', 1.00);
INSERT INTO `dealer_rate`
VALUES (2, 'ＳＢ/皇冠', 0.98);
INSERT INTO `dealer_rate`
VALUES (3, 'Bet365', 0.87);
INSERT INTO `dealer_rate`
VALUES (4, '易胜博', 0.9);
INSERT INTO `dealer_rate`
VALUES (5, '韦德', 0.78);
INSERT INTO `dealer_rate`
VALUES (6, '明陞', 0.84);
INSERT INTO `dealer_rate`
VALUES (7, '10BET', 0.67);
INSERT INTO `dealer_rate`
VALUES (8, '金宝博', 0.54);
INSERT INTO `dealer_rate`
VALUES (9, '12bet/沙巴', 0.77);
INSERT INTO `dealer_rate`
VALUES (10, '利记', 0.93);
INSERT INTO `dealer_rate`
VALUES (11, '盈禾', 0.91);
INSERT INTO `dealer_rate`
VALUES (12, '18bet', 0.49);
INSERT INTO `dealer_rate`
VALUES (13, '平博', 0.59);
INSERT INTO `dealer_rate`
VALUES (14, '澳门', 0.58);
INSERT INTO `dealer_rate`
VALUES (15, '香港马会', 0.74);

-- ----------------------------
-- Table structure for hedge
-- ----------------------------
DROP TABLE IF EXISTS `hedge`;
CREATE TABLE `hedge`
(
    `id`         int(11) UNSIGNED                                    NOT NULL AUTO_INCREMENT,
    `sport`      char(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin   NOT NULL,
    `league`     char(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin  NOT NULL,
    `event_1`    char(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin  NOT NULL,
    `event_2`    char(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL,
    `event_3`    char(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL,
    `dtime`      datetime(6)                                         NOT NULL,
    `dealer_1`   char(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin  NOT NULL,
    `dealer_2`   char(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin  NOT NULL,
    `dealer_3`   char(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin  NOT NULL,
    `handicap_1` float(4, 2)                                         NOT NULL,
    `handicap_2` float(4, 2)                                         NOT NULL,
    `handicap_3` float(4, 2)                                         NOT NULL,
    `odd_1`      float(4, 2)                                         NOT NULL,
    `odd_2`      float(4, 2)                                         NOT NULL,
    `odd_draw`   float(5, 2)                                         NOT NULL,
    `pending_a`  int(11)                                             NOT NULL,
    `pending_b`  int(11)                                             NOT NULL,
    `pending_c`  int(11)                                             NOT NULL,
    `gain`       int(11)                                             NOT NULL,
    PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB
  AUTO_INCREMENT = 1
  CHARACTER SET = utf8mb4
  COLLATE = utf8mb4_bin
  ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for jc_to_asia
-- ----------------------------
DROP TABLE IF EXISTS `jc_to_asia`;
CREATE TABLE `jc_to_asia`
(
    `id`          int(11) UNSIGNED                                   NOT NULL AUTO_INCREMENT,
    `event`       char(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL,
    `event_en`    char(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL,
    `event_id`    int(11) UNSIGNED                                   NOT NULL,
    `dealer`      char(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL,
    `odd_1`       float(4, 2)                                        NOT NULL,
    `odd_2`       float(4, 2)                                        NOT NULL,
    `odd_draw`    float(5, 2)                                        NOT NULL,
    `status`      smallint(5) UNSIGNED                               NOT NULL,
    `start_time`  datetime(6)                                        NOT NULL,
    `update_time` datetime(6)                                        NOT NULL,
    `handicap`    float(4, 2)                                        NOT NULL,
    `sports`      char(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin  NOT NULL,
    `league`      char(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL,
    PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB
  AUTO_INCREMENT = 1
  CHARACTER SET = utf8mb4
  COLLATE = utf8mb4_bin
  ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for odds
-- ----------------------------
DROP TABLE IF EXISTS `odds`;
CREATE TABLE `odds`
(
    `id`          int(11) UNSIGNED                                    NOT NULL AUTO_INCREMENT,
    `event`       char(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin  NOT NULL,
    `event_en`    char(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL,
    `event_id`    int(11) UNSIGNED                                    NOT NULL,
    `dealer`      char(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin  NOT NULL,
    `odd_1`       float(4, 2)                                         NOT NULL,
    `odd_2`       float(4, 2)                                         NOT NULL,
    `odd_draw`    float(5, 2)                                         NOT NULL,
    `status`      smallint(6) UNSIGNED                                NOT NULL,
    `start_time`  datetime(6)                                         NOT NULL,
    `update_time` datetime(6)                                         NOT NULL,
    `handicap`    float(4, 2)                                         NOT NULL,
    `sports`      char(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin   NOT NULL,
    `league`      char(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin  NOT NULL,
    PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB
  AUTO_INCREMENT = 1
  CHARACTER SET = utf8mb4
  COLLATE = utf8mb4_bin
  ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for on_bet
-- ----------------------------
DROP TABLE IF EXISTS `on_bet`;
CREATE TABLE `on_bet`
(
    `id`         int(11) UNSIGNED                                    NOT NULL AUTO_INCREMENT,
    `sport`      char(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin   NOT NULL,
    `league`     char(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin  NOT NULL,
    `event_1`    char(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin  NOT NULL,
    `event_2`    char(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL,
    `event_3`    char(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin   NOT NULL,
    `event_id`   int(11) UNSIGNED                                    NOT NULL,
    `dtime`      datetime(6)                                         NOT NULL,
    `dealer_1`   char(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin  NOT NULL,
    `dealer_2`   char(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin  NOT NULL,
    `dealer_3`   char(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin  NOT NULL,
    `handicap_1` float(4, 2)                                         NOT NULL,
    `handicap_2` float(4, 2)                                         NOT NULL,
    `handicap_3` float(4, 2)                                         NOT NULL,
    `odd_1`      float(4, 2)                                         NOT NULL,
    `odd_2`      float(4, 2)                                         NOT NULL,
    `odd_draw`   float(5, 2)                                         NOT NULL,
    `pending_a`  int(11)                                             NOT NULL,
    `pending_b`  int(11)                                             NOT NULL,
    `pending_c`  int(11)                                             NOT NULL,
    `gain`       int(11)                                             NOT NULL,
    `diff_1`     float(4, 2)                                         NOT NULL,
    `diff_2`     float(4, 2)                                         NOT NULL,
    `balance_1`  float(4, 2)                                         NOT NULL,
    `balance_2`  float(4, 2)                                         NOT NULL,
    `status`     smallint(6) UNSIGNED                                NOT NULL,
    PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB
  AUTO_INCREMENT = 1
  CHARACTER SET = utf8mb4
  COLLATE = utf8mb4_bin
  ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for wy_hedge
-- ----------------------------
DROP TABLE IF EXISTS `wy_hedge`;
CREATE TABLE `wy_hedge`
(
    `id`         int(11) UNSIGNED                                    NOT NULL AUTO_INCREMENT,
    `sport`      char(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin   NOT NULL,
    `league`     char(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin  NOT NULL,
    `event_1`    char(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin  NOT NULL,
    `event_2`    char(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL,
    `event_3`    char(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL,
    `dtime`      datetime(6)                                         NOT NULL,
    `dealer_1`   char(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin  NOT NULL,
    `dealer_2`   char(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin  NOT NULL,
    `dealer_3`   char(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin  NOT NULL,
    `handicap_1` float(4, 2)                                         NOT NULL,
    `handicap_2` float(4, 2)                                         NOT NULL,
    `handicap_3` float(4, 2)                                         NOT NULL,
    `odd_1`      float(4, 2)                                         NOT NULL,
    `odd_2`      float(4, 2)                                         NOT NULL,
    `odd_draw`   float(5, 2)                                         NOT NULL,
    `pending_a`  int(11)                                             NOT NULL,
    `pending_b`  int(11)                                             NOT NULL,
    `pending_c`  int(11)                                             NOT NULL,
    `gain`       int(11)                                             NOT NULL,
    PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB
  AUTO_INCREMENT = 1
  CHARACTER SET = utf8mb4
  COLLATE = utf8mb4_bin
  ROW_FORMAT = Dynamic;

SET FOREIGN_KEY_CHECKS = 1;
