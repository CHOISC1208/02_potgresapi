import os
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)

# "postgres://"を"postgresql://"に置換する
database_uri = os.getenv('DATABASE_URL')
if database_uri:
    database_uri = database_uri.replace('postgres://', 'postgresql://', 1)
else:
    # ローカル環境用のデフォルト値
    # 提供されたHeroku Postgresの情報をデフォルト値として使用
    database_uri = 'postgresql://ue1c7b1j0pjfal:p65045f16ae3b2f2a1a121bddc8c0bed0b986fa452e4d822bd56f45ab96ceda85@c7gljno857ucsl.cluster-czrs8kj4isg7.us-east-1.rds.amazonaws.com:5432/d936cvvhfj3ecg'

app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# B_recipes モデルの定義
class B_recipes(db.Model):
    __tablename__ = 'b_recipes'
    recipe_id = db.Column(db.String(255), primary_key=True)  # プライマリキーとして recipe_id を使用
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    video_time = db.Column(db.String(8))
    view_count = db.Column(db.Integer)
    published_at = db.Column(db.TIMESTAMP(timezone=True))
    updated_at = db.Column(db.TIMESTAMP(timezone=True), default=db.func.current_timestamp())
    thumbnail_url = db.Column(db.String(255))

# 新しいルート定義を追加
@app.route('/')
def home():
    return 'Hello, World!'

# /recipes エンドポイントの定義
@app.route('/recipes', methods=['GET'])
def get_recipes():
    try:
        recipes = B_recipes.query.all()  # 正しい、問題ないクエリ
        recipe_data = [{
            'recipe_id': recipe.recipe_id,
            'title': recipe.title,
            'description': recipe.description,
            'video_time': recipe.video_time,
            'view_count': recipe.view_count,
            'published_at': recipe.published_at.isoformat() if recipe.published_at else None,
            'updated_at': recipe.updated_at.isoformat() if recipe.updated_at else None,
            'thumbnail_url': recipe.thumbnail_url
        } for recipe in recipes]
        
        return jsonify(recipe_data)
    except Exception as e:
        app.logger.error(f"Error fetching recipes: {e}")
        return jsonify({"error": "Internal Server Error"}), 500


if __name__ == '__main__':
    app.run(debug=True)
