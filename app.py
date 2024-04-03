import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)

# HerokuからのDATABASE_URLを取得し、"postgres://" を "postgresql://" に置換する
database_uri = os.getenv('DATABASE_URL').replace('postgres://', 'postgresql://', 1)
app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
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
    app.run()