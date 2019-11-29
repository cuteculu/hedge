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

 Date: 26/11/2019 23:51:44
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for dealer_rate
-- ----------------------------
DROP TABLE IF EXISTS `dealer_rate`;
CREATE TABLE `dealer_rate`  (
  `id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT,
  `dealer` char(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL,
  `rate` float(5, 2) UNSIGNED NOT NULL DEFAULT 0.00,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 16 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_bin ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of dealer_rate
-- ----------------------------
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

SET FOREIGN_KEY_CHECKS = 1;
