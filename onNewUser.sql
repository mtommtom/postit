INSERT INTO users (userName, userPassword)
VALUES (:name, :password);

-- on click post post
INSERT INTO posts (user_id, img, description, likes)
VALUES (:user_id, :img, :description, :likes);