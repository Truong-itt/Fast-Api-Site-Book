-- Bảng lưu thông tin người dùng
CREATE TABLE IF NOT EXISTS users (
    user_id SERIAL PRIMARY KEY,    -- ID tự động tăng
    name VARCHAR(100) NOT NULL,    -- Tên người dùng
    email VARCHAR(100) UNIQUE NOT NULL, -- Email (duy nhất)
    password VARCHAR(255) NOT NULL, -- Mật khẩu (hashed)
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- Thời gian tạo
);

-- Bảng lưu danh mục sách (nếu có)
CREATE TABLE IF NOT EXISTS categories (
    category_id SERIAL PRIMARY KEY, -- ID danh mục
    name VARCHAR(100) NOT NULL UNIQUE -- Tên danh mục
);

-- Bảng lưu thông tin sách
CREATE TABLE IF NOT EXISTS books (
    book_id SERIAL PRIMARY KEY,    -- ID sách (tự động tăng)
    title VARCHAR(255) NOT NULL,   -- Tên sách
    author VARCHAR(255) NOT NULL,  -- Tác giả
    description TEXT,              -- Mô tả sách
    price DECIMAL(10, 2) NOT NULL, -- Giá sách
    stock INT DEFAULT 0,           -- Số lượng trong kho
    category_id INT,               -- ID danh mục
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Thời gian tạo
    FOREIGN KEY (category_id) REFERENCES categories(category_id) -- Khóa ngoại tới bảng categories
);

-- Bảng lưu thông tin đơn hàng
CREATE TABLE IF NOT EXISTS orders (
    order_id SERIAL PRIMARY KEY,   -- ID đơn hàng (tự động tăng)
    user_id INT NOT NULL,          -- Người thực hiện đơn hàng
    total_amount DECIMAL(10, 2) NOT NULL, -- Tổng số tiền
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Thời gian tạo
    status VARCHAR(50) DEFAULT 'pending', -- Trạng thái đơn hàng
    FOREIGN KEY (user_id) REFERENCES users(user_id) -- Ràng buộc khóa ngoại tới bảng users
);

-- Bảng lưu chi tiết đơn hàng
CREATE TABLE IF NOT EXISTS order_items (
    order_item_id SERIAL PRIMARY KEY, -- ID chi tiết đơn hàng
    order_id INT NOT NULL,            -- ID đơn hàng
    book_id INT NOT NULL,             -- ID sách
    quantity INT NOT NULL,            -- Số lượng
    price DECIMAL(10, 2) NOT NULL,    -- Giá tại thời điểm đặt hàng
    FOREIGN KEY (order_id) REFERENCES orders(order_id), -- Ràng buộc khóa ngoại tới bảng orders
    FOREIGN KEY (book_id) REFERENCES books(book_id)     -- Ràng buộc khóa ngoại tới bảng books
);

-- Bảng lưu đánh giá sách (tùy chọn)
CREATE TABLE IF NOT EXISTS reviews (
    review_id SERIAL PRIMARY KEY,    -- ID đánh giá
    book_id INT NOT NULL,            -- ID sách
    user_id INT NOT NULL,            -- ID người dùng
    rating INT CHECK (rating >= 1 AND rating <= 5), -- Đánh giá (1-5 sao)
    comment TEXT,                    -- Bình luận
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Thời gian tạo
    FOREIGN KEY (book_id) REFERENCES books(book_id), -- Ràng buộc khóa ngoại tới bảng books
    FOREIGN KEY (user_id) REFERENCES users(user_id) -- Ràng buộc khóa ngoại tới bảng users
);
