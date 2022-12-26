from flask import Flask,request #pip install flask
from flask_restful import Resource,Api,abort,reqparse,fields,marshal_with #pip install flask-restful
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)
api=Api(app)
app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:c98xa5@localhost:5432/flaskapi'
db=SQLAlchemy(app)
app.app_context().push()

class TodoModel(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    task=db.Column(db.String(200))
    summary=db.Column(db.String(500))
"""
db.create_all()

@app.route("/")
def home_page():
    return "Hello World"

class Hello(Resource):

    def get(self):
        return {'hello':'world'}
api.add_resource(Hello,'/user/')

todos={
    1:{"task":"Write hello world program","summary":"Write the code using python"}
}
"""
task_post_args=reqparse.RequestParser()
task_post_args.add_argument("task",type=str,help="Task is required",required=True)
task_post_args.add_argument("summary",type=str,help="Summary is required",required=True)

task_put_args=reqparse.RequestParser()
task_put_args.add_argument("task",type=str)
task_put_args.add_argument("summary",type=str)

resource_fields={
    'id':fields.Integer,
    'task':fields.String,
    'summary':fields.String
}

class TodoList(Resource):
    def get(self):
        tasks=TodoModel.query.all()
        todos={}
        for task in tasks:
            todos[task.id]={"task":task.task,"summary":task.summary}
        return todos
        
class Todos(Resource):
    @marshal_with(resource_fields)
    def get(self,todo_id):
        task=TodoModel.query.filter_by(id=todo_id).first()
        if task==None:
            abort("task not there")
        return task
    @marshal_with(resource_fields)
    def post(self,todo_id):
        args=task_post_args.parse_args()
        task=TodoModel.query.filter_by(id=todo_id).first()
        if task:
            abort(409,'Task ID already taken')
        todo=TodoModel(id=todo_id,task=args['task'],summary=args['summary'])
        db.session.add(todo)
        db.session.commit()
        return todo,201
    @marshal_with(resource_fields)
    def put(self,todo_id):
        args=task_put_args.parse_args()
        task=TodoModel.query.filter_by(id=todo_id).first()
        if not task:
            abort(404,'Task does not exist cannot update')
        if args['task']:
            task.task=args['task']
        if args['summary']: 
            task.summary=args['summary']
        db.session.commit()
        return task
        
    def delete(self,todo_id):
        task=TodoModel.query.filter_by(id=todo_id).first()
        db.session.delete(task)
        db.session.commit()
        return "Todo Deleted",204
        
api.add_resource(TodoList, '/todos')
api.add_resource(Todos, '/todos/<int:todo_id>')

if __name__=='__main__':
    app.run(debug=True)