-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: May 17, 2025 at 12:25 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `inventory_db`
--

-- --------------------------------------------------------

--
-- Table structure for table `activity_log`
--

CREATE TABLE `activity_log` (
  `id` int(11) NOT NULL,
  `description` text NOT NULL,
  `created_at` datetime NOT NULL,
  `user_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `activity_log`
--

INSERT INTO `activity_log` (`id`, `description`, `created_at`, `user_id`) VALUES
(8, 'Order #5 placed: RTX 580 (Qty: 12)', '2025-05-16 02:35:38', 1),
(9, 'Order #6 placed: HP monitor (Qty: 20)', '2025-05-16 02:40:37', 1),
(10, 'Order #6 status updated to Completed', '2025-05-16 02:41:20', 1),
(11, 'Order #5 status updated to Cancelled', '2025-05-16 03:06:40', 1),
(12, 'Low stock alert: 1 items below threshold (10)', '2025-05-16 13:18:20', 1),
(13, 'Order #7 placed: RTX 580 (Qty: 10)', '2025-05-16 13:57:36', 1),
(14, 'Order #7 status updated to Completed', '2025-05-16 13:57:52', 1),
(15, 'Order #8 placed: RTX 580 (Qty: 100)', '2025-05-16 14:24:54', 1),
(16, 'Order #8 status updated to Completed', '2025-05-16 14:25:07', 1),
(17, 'Stock out: 12 of RTX 580', '2025-05-16 14:40:59', 1),
(18, 'Stock out: 23 of RTX 580', '2025-05-16 14:41:22', 1),
(19, 'Order #9 placed: Hp (Qty: 100), RTX 5890 (Qty: 50)', '2025-05-16 14:54:51', 1),
(20, 'Order #9 status updated to Completed', '2025-05-16 14:55:32', 1),
(21, 'Stock out: 20 of RTX 5890', '2025-05-16 15:03:37', 1),
(22, 'Order #10 placed: Hp (Qty: 10)', '2025-05-16 15:20:26', 2),
(23, 'Order #11 placed: Hp (Qty: 10)', '2025-05-16 17:02:01', 2),
(24, 'Order #12 placed: RTX 580 (Qty: 10)', '2025-05-16 17:04:36', 1),
(25, 'Order #13 placed: RTX 580 (Qty: 12)', '2025-05-16 17:05:35', 1),
(26, 'Order #14 placed: RTX 580 (Qty: 1)', '2025-05-16 17:10:34', 2),
(27, 'Order #15 placed: RTX 580 (Qty: 10), RTX 5890 (Qty: 10)', '2025-05-16 17:26:22', 1),
(28, 'Order #16 placed: RTX 5890 (Qty: 12)', '2025-05-16 17:26:47', 1),
(29, 'Order #10 status updated to Completed', '2025-05-16 17:27:04', 1),
(30, 'Order #16 status updated to Completed', '2025-05-16 17:28:19', 2),
(31, 'Order #15 status updated to Completed', '2025-05-16 17:39:52', 1),
(32, 'Order #14 status updated to Completed', '2025-05-16 17:40:06', 1),
(33, 'Stock out: 10 of Hp', '2025-05-16 19:08:24', 2),
(34, 'Order #20 placed: AMD Ryzen 7 9800X3D (Qty: 10)', '2025-05-16 19:25:09', 1),
(35, 'Order #20 status updated to Completed', '2025-05-16 19:25:20', 1),
(36, 'Stock out: 20 of Hp', '2025-05-16 19:27:17', 1),
(37, 'Stock out: 2 of AMD Ryzen 7 9800X3D', '2025-05-16 19:27:31', 1),
(38, 'Stock out: 10 of Hp', '2025-05-16 19:27:48', 1),
(39, 'Order #21 placed: Amd (Qty: 1)', '2025-05-17 14:12:09', 1),
(40, 'Order #21 status updated to Cancelled', '2025-05-17 18:08:37', 1),
(41, 'Order #13 status updated to Completed', '2025-05-17 18:08:53', 1),
(42, 'Order #22 placed: AMD Ryzen 7 9800X3D (Qty: 10), Amd (Qty: 10)', '2025-05-17 18:09:37', 1),
(43, 'Stock out: 20 of RTX 580', '2025-05-17 18:10:28', 1),
(44, 'Order #22 status updated to Completed', '2025-05-17 18:14:41', 2),
(45, 'Order #12 status updated to Cancelled', '2025-05-17 18:14:52', 2),
(46, 'Order #23 placed: Amd (Qty: 12), RTX 580 (Qty: 13)', '2025-05-17 18:15:18', 2),
(47, 'Stock out: 12 of AMD Ryzen 7 9800X3D', '2025-05-17 18:15:44', 2);

-- --------------------------------------------------------

--
-- Table structure for table `categories`
--

CREATE TABLE `categories` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `description` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `categories`
--

INSERT INTO `categories` (`id`, `name`, `description`) VALUES
(1, 'GPU', 'Graphics Card'),
(3, 'Monitor', 'Monitor'),
(4, 'Mouse', 'Mouse'),
(5, 'CPU', 'Central Processing Unit');

-- --------------------------------------------------------

--
-- Table structure for table `orders`
--

CREATE TABLE `orders` (
  `id` int(11) NOT NULL,
  `supplier_id` int(11) NOT NULL,
  `order_date` datetime NOT NULL,
  `status` enum('Pending','Completed','Cancelled') DEFAULT 'Pending'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `orders`
--

INSERT INTO `orders` (`id`, `supplier_id`, `order_date`, `status`) VALUES
(5, 2, '2025-05-16 02:35:37', 'Cancelled'),
(6, 2, '2025-05-16 02:40:34', 'Completed'),
(7, 1, '2025-05-16 13:57:34', 'Completed'),
(8, 2, '2025-05-16 14:24:53', 'Completed'),
(9, 2, '2025-05-16 14:54:49', 'Completed'),
(10, 2, '2025-05-16 15:20:25', 'Completed'),
(11, 2, '2025-05-16 17:02:00', 'Pending'),
(12, 2, '2025-05-16 17:04:35', 'Cancelled'),
(13, 2, '2025-05-16 17:05:34', 'Completed'),
(14, 1, '2025-05-16 17:10:33', 'Completed'),
(15, 2, '2025-05-16 17:26:21', 'Completed'),
(16, 2, '2025-05-16 17:26:46', 'Completed'),
(20, 1, '2025-05-16 19:25:07', 'Completed'),
(21, 4, '2025-05-17 14:12:08', 'Cancelled'),
(22, 1, '2025-05-17 18:09:34', 'Completed'),
(23, 4, '2025-05-17 18:15:17', 'Pending');

-- --------------------------------------------------------

--
-- Table structure for table `order_items`
--

CREATE TABLE `order_items` (
  `id` int(11) NOT NULL,
  `order_id` int(11) NOT NULL,
  `part_id` int(11) NOT NULL,
  `quantity` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `order_items`
--

INSERT INTO `order_items` (`id`, `order_id`, `part_id`, `quantity`) VALUES
(8, 5, 5, 12),
(10, 7, 5, 10),
(11, 8, 5, 100),
(12, 9, 9, 100),
(13, 9, 10, 50),
(14, 10, 9, 10),
(15, 11, 9, 10),
(16, 12, 5, 10),
(17, 13, 5, 12),
(18, 14, 5, 1),
(19, 15, 5, 10),
(20, 15, 10, 10),
(21, 16, 10, 12),
(26, 20, 23, 10),
(27, 21, 24, 1),
(28, 22, 23, 10),
(29, 22, 24, 10),
(30, 23, 24, 12),
(31, 23, 5, 13);

-- --------------------------------------------------------

--
-- Table structure for table `parts`
--

CREATE TABLE `parts` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `quantity` int(11) NOT NULL,
  `price` decimal(10,2) NOT NULL,
  `category_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `parts`
--

INSERT INTO `parts` (`id`, `name`, `quantity`, `price`, `category_id`) VALUES
(5, 'RTX 580', 3, 200.00, 1),
(9, 'Hp', 70, 10000.00, 3),
(10, 'RTX 5890', 52, 200.00, 1),
(12, 'Acer', 0, 2000.00, 3),
(13, 'Asus', 0, 2500.00, 3),
(14, 'Samsung', 0, 5000.00, 3),
(15, 'Dell', 0, 5000.00, 3),
(16, 'Lg ', 0, 5000.00, 3),
(17, 'Razer Basilisk', 0, 5000.00, 4),
(18, 'Logitech Mx', 0, 2500.00, 4),
(19, 'Razer Pro Click', 0, 3000.00, 4),
(20, 'Microsoft Adaptive Mouse', 0, 3000.00, 4),
(21, 'Amd ', 0, 5000.00, 1),
(22, 'Nvidia', 0, 5000.00, 1),
(23, 'AMD Ryzen 7 9800X3D', 6, 5800.00, 5),
(24, 'Amd', 10, 123.00, 5),
(25, 'Amd Cpu', 0, 2000.00, 5);

-- --------------------------------------------------------

--
-- Table structure for table `stock_alerts`
--

CREATE TABLE `stock_alerts` (
  `id` int(11) NOT NULL,
  `part_id` int(11) DEFAULT NULL,
  `alert_date` datetime DEFAULT NULL,
  `status` varchar(20) DEFAULT NULL,
  `acknowledged_by` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `stock_outs`
--

CREATE TABLE `stock_outs` (
  `id` int(11) NOT NULL,
  `part_id` int(11) NOT NULL,
  `quantity` int(11) NOT NULL,
  `processed_date` date NOT NULL,
  `user_id` int(11) DEFAULT NULL
) ;

--
-- Dumping data for table `stock_outs`
--

INSERT INTO `stock_outs` (`id`, `part_id`, `quantity`, `processed_date`, `user_id`) VALUES
(1, 5, 12, '2025-05-16', 1),
(2, 5, 23, '2025-05-16', 1),
(3, 10, 20, '2025-05-16', 1),
(4, 9, 10, '2025-05-16', 2),
(5, 9, 20, '2025-05-16', 1),
(6, 23, 2, '2025-05-16', 1),
(7, 9, 10, '2025-05-16', 1),
(8, 5, 20, '2025-05-17', 1),
(9, 23, 12, '2025-05-17', 2);

-- --------------------------------------------------------

--
-- Table structure for table `suppliers`
--

CREATE TABLE `suppliers` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `contact` varchar(255) NOT NULL,
  `address` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `suppliers`
--

INSERT INTO `suppliers` (`id`, `name`, `contact`, `address`) VALUES
(1, 'N', '9696176980', 'MAA'),
(2, 'Gaisano', '09286176980', 'Calinan'),
(4, 'Abreeza', '09111111111', 'Tugbok'),
(5, 'Gaisano Grand', '09111111111', 'Calinan');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `username` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `role` enum('Admin','Inventory Staff') NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `username`, `password`, `role`) VALUES
(1, 'admin', '$2b$12$n/ADkHUTHO9OcJSh5KY7EOOLimccqphfUYdLLeZc3.jsv61OFYmm6', 'Admin'),
(2, 'staff', '$2b$12$cHbDpb1Lh6s9k1XKipRVi.vS/vix1IbB.UZpvADMEmxNlpK3ft4cC', 'Inventory Staff');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `activity_log`
--
ALTER TABLE `activity_log`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `categories`
--
ALTER TABLE `categories`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `uk_name` (`name`);

--
-- Indexes for table `orders`
--
ALTER TABLE `orders`
  ADD PRIMARY KEY (`id`),
  ADD KEY `supplier_id` (`supplier_id`);

--
-- Indexes for table `order_items`
--
ALTER TABLE `order_items`
  ADD PRIMARY KEY (`id`),
  ADD KEY `order_id` (`order_id`),
  ADD KEY `part_id` (`part_id`);

--
-- Indexes for table `parts`
--
ALTER TABLE `parts`
  ADD PRIMARY KEY (`id`),
  ADD KEY `fk_category` (`category_id`);

--
-- Indexes for table `stock_alerts`
--
ALTER TABLE `stock_alerts`
  ADD PRIMARY KEY (`id`),
  ADD KEY `part_id` (`part_id`);

--
-- Indexes for table `stock_outs`
--
ALTER TABLE `stock_outs`
  ADD PRIMARY KEY (`id`),
  ADD KEY `part_id` (`part_id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `suppliers`
--
ALTER TABLE `suppliers`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `activity_log`
--
ALTER TABLE `activity_log`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=48;

--
-- AUTO_INCREMENT for table `categories`
--
ALTER TABLE `categories`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `orders`
--
ALTER TABLE `orders`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=24;

--
-- AUTO_INCREMENT for table `order_items`
--
ALTER TABLE `order_items`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=32;

--
-- AUTO_INCREMENT for table `parts`
--
ALTER TABLE `parts`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=26;

--
-- AUTO_INCREMENT for table `stock_alerts`
--
ALTER TABLE `stock_alerts`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `stock_outs`
--
ALTER TABLE `stock_outs`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `suppliers`
--
ALTER TABLE `suppliers`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `activity_log`
--
ALTER TABLE `activity_log`
  ADD CONSTRAINT `activity_log_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);

--
-- Constraints for table `orders`
--
ALTER TABLE `orders`
  ADD CONSTRAINT `orders_ibfk_1` FOREIGN KEY (`supplier_id`) REFERENCES `suppliers` (`id`);

--
-- Constraints for table `order_items`
--
ALTER TABLE `order_items`
  ADD CONSTRAINT `order_items_ibfk_1` FOREIGN KEY (`order_id`) REFERENCES `orders` (`id`),
  ADD CONSTRAINT `order_items_ibfk_2` FOREIGN KEY (`part_id`) REFERENCES `parts` (`id`);

--
-- Constraints for table `parts`
--
ALTER TABLE `parts`
  ADD CONSTRAINT `fk_category` FOREIGN KEY (`category_id`) REFERENCES `categories` (`id`);

--
-- Constraints for table `stock_alerts`
--
ALTER TABLE `stock_alerts`
  ADD CONSTRAINT `stock_alerts_ibfk_1` FOREIGN KEY (`part_id`) REFERENCES `parts` (`id`);

--
-- Constraints for table `stock_outs`
--
ALTER TABLE `stock_outs`
  ADD CONSTRAINT `stock_outs_ibfk_1` FOREIGN KEY (`part_id`) REFERENCES `parts` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `stock_outs_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE SET NULL;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
