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




INSERT INTO users (name, email, password)
VALUES 
('Alice', 'alice@example.com', 'hashed_password_1'),
('Bob', 'bob@example.com', 'hashed_password_2'),
('Charlie', 'charlie@example.com', 'hashed_password_3');




INSERT INTO categories (name)
VALUES 
('Fiction'),
('Non-fiction'),
('Science'),
('History'),
('Biography'),
('Fantasy'),
('Mystery'),
('Romance'),
('Self-help'),
('Technology');


INSERT INTO books (title, author, description, price, stock, category_id)
VALUES
('The Great Gatsby', 'F. Scott Fitzgerald', 'A novel about the American dream.', 10.99, 50, 1),
('To Kill a Mockingbird', 'Harper Lee', 'A story of racial injustice.', 12.50, 30, 2),
('Brief History of Time', 'Stephen Hawking', 'An overview of cosmology.', 15.99, 20, 3),
('Sapiens: A Brief History of Humankind', 'Yuval Noah Harari', 'A historical exploration of humanity.', 18.99, 25, 4),
('Steve Jobs', 'Walter Isaacson', 'Biography of Steve Jobs.', 22.99, 15, 5),
('Harry Potter and the Philosopher''s Stone', 'J.K. Rowling', 'The first book in the Harry Potter series.', 8.99, 100, 6),
('The Hobbit', 'J.R.R. Tolkien', 'A prelude to The Lord of the Rings.', 14.50, 40, 6),
('Gone Girl', 'Gillian Flynn', 'A psychological thriller novel.', 11.99, 35, 7),
('The Da Vinci Code', 'Dan Brown', 'A symbologist unravels secrets.', 13.50, 45, 7),
('Pride and Prejudice', 'Jane Austen', 'A classic romance novel.', 9.99, 60, 8),
('The Fault in Our Stars', 'John Green', 'A touching story of love and illness.', 10.50, 55, 8),
('Atomic Habits', 'James Clear', 'A guide to building good habits.', 16.99, 30, 9),
('The 7 Habits of Highly Effective People', 'Stephen Covey', 'A self-help classic.', 17.99, 25, 9),
('Clean Code', 'Robert C. Martin', 'Best practices for writing clean code.', 29.99, 20, 10),
('The Pragmatic Programmer', 'Andrew Hunt', 'Programming wisdom and practices.', 27.50, 15, 10),
('1984', 'George Orwell', 'A dystopian novel.', 10.99, 50, 1),
('Educated', 'Tara Westover', 'A memoir about overcoming ignorance.', 13.99, 30, 5),
('The Alchemist', 'Paulo Coelho', 'A journey of self-discovery.', 12.99, 40, 8),
('Dune', 'Frank Herbert', 'A sci-fi masterpiece.', 15.50, 25, 6),
('The Art of War', 'Sun Tzu', 'Ancient wisdom on strategy.', 11.50, 35, 4);


INSERT INTO orders (user_id, total_amount, status)
VALUES 
(1, 52.47, 'completed'),
(2, 45.99, 'pending'),
(3, 78.50, 'shipped'),
(1, 99.99, 'completed'),
(2, 120.50, 'cancelled'),
(3, 65.75, 'processing'),
(1, 30.25, 'completed'),
(2, 85.00, 'pending'),
(3, 50.49, 'shipped'),
(1, 70.00, 'completed');


INSERT INTO order_items (order_id, book_id, quantity, price)
VALUES
(1, 1, 2, 21.98),
(1, 3, 1, 15.99),
(2, 2, 1, 12.50),
(2, 4, 1, 18.99),
(3, 5, 2, 45.98),
(3, 6, 1, 8.99),
(4, 7, 3, 43.50),
(4, 8, 1, 11.99),
(5, 9, 2, 27.00),
(5, 10, 1, 9.99),
(6, 11, 1, 10.50),
(6, 12, 2, 33.98),
(7, 13, 1, 17.99),
(7, 14, 1, 29.99),
(8, 15, 1, 27.50),
(8, 16, 2, 21.98),
(9, 17, 1, 13.99),
(9, 18, 1, 12.99),
(10, 19, 1, 15.50),
(10, 20, 1, 11.50);


INSERT INTO reviews (book_id, user_id, rating, comment)
VALUES
(1, 1, 5, 'A timeless classic. Loved every bit of it.'),
(2, 2, 4, 'Well-written but a bit slow in the middle.'),
(3, 3, 5, 'Fascinating insights into the universe.'),
(4, 1, 4, 'Very informative and thought-provoking.'),
(5, 2, 5, 'An inspiring biography.'),
(6, 3, 5, 'Absolutely magical. A must-read for all ages.'),
(7, 1, 4, 'A thrilling adventure.'),
(8, 2, 3, 'Interesting plot, but predictable ending.'),
(9, 3, 4, 'A good blend of history and fiction.'),
(10, 1, 5, 'Romantic and heartwarming.'),
(11, 2, 4, 'A tear-jerker, but worth it.'),
(12, 3, 5, 'Life-changing advice on habits.'),
(13, 1, 4, 'Some repetitive points, but overall helpful.'),
(14, 2, 5, 'Essential reading for programmers.'),
(15, 3, 5, 'Great resource for developers.'),
(16, 1, 4, 'Still relevant in today’s world.'),
(17, 2, 5, 'A moving and inspirational memoir.'),
(18, 3, 4, 'Simple yet powerful message.'),
(19, 1, 5, 'An epic science fiction journey.'),
(20, 2, 4, 'Strategic lessons still hold value today.');
