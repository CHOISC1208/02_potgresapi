import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)

# Heroku環境変数からデータベースURLを取得し、必要に応じてスキームを置き換えます。
uri = os.getenv('DATABASE_URL')  # or other relevant config var
if uri and uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)

app.config['SQLALCHEMY_DATABASE_URI'] = uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# テーブル名とフィールド名を辞書で定義
tables = {
    'a_contributor': {'name': db.String(128)},
    'b_recipes': {'title': db.String(128)},
    'c_materials': {'material': db.String(128)},
    'd_steps': {'step': db.String(128)},
    'e_recipedetail': {'detail': db.String(128)}
}

def create_model(table_name, columns):
    """動的にモデルクラスを生成する関数"""
    attrs = {'__tablename__': table_name, '__table_args__': {'extend_existing': True}}
    # IDカラムとその他のカラムを追加
    attrs['id'] = db.Column(db.Integer, primary_key=True)
    for column_name, column_type in columns.items():
        attrs[column_name] = db.Column(column_type)
    return type(table_name.capitalize(), (db.Model,), attrs)

# テーブル名を基にモデルを生成
for table_name, columns in tables.items():
    model = create_model(table_name, columns)
    globals()[model.__name__] = model

if __name__ == '__main__':
    app.run(debug=True)
