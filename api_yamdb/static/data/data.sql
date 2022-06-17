.mode csv
.separator ,
.import --skip 1 api_yamdb/static/data/category.csv reviews_category
.import --skip 1 api_yamdb/static/data/comments.csv reviews_comment
.import --skip 1 api_yamdb/static/data/genre_title.csv reviews_title_genre
.import --skip 1 api_yamdb/static/data/genre.csv reviews_genre
.import --skip 1 api_yamdb/static/data/review.csv reviews_review
.import --skip 1 api_yamdb/static/data/titles.csv reviews_title
.import --skip 1 api_yamdb/static/data/users.csv reviews_user
