from pylon.frame import App
from armory.tank.mysql import ArmoryOrm

from barracks.app import Barracks

app = App(__name__)
app.config['DEBUG'] = True
app.config[
    'db'] = 'mysql://root:123456@localhost:3306/flask_restless?charset=utf8'
db = ArmoryOrm()
db.init_app(app)


class Person(db.Model):
    __tablename__ = "person"
    __session__ = db.session
    __filters__ = {
        'multi': ['name']
    }
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.VARCHAR(32))
    birth_date = db.Column(db.Date)
    computers = db.relationship('Computer', backref='person')


class Computer(db.Model):
    __tablename__ = "computer"
    __session__ = db.session
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.VARCHAR(32))
    vendor = db.Column(db.VARCHAR(32))
    purchase_time = db.Column(db.DateTime)
    owner_id = db.Column(db.Integer, db.ForeignKey('person.id'))
    owner = db.relationship('Person')


if __name__ == '__main__':
    def test_api():
        print 'test api!!!'
        return 'test api!!!'
    model_list = [Person, Computer]
    app_conf = {}
    barracks_app = Barracks('test')
    barracks_app.init_conf(app_conf, model_list, debug=True)
    # barracks_app.add_data(Person, {'name': 'sssxxx', 'birth_date': '2014-01-01', 'computers': [
    #                       {'name': 'ibm1', 'vendor': 'ibm', 'purchase_time': '2015-01-01 00:00:00'}]})
    # print barracks_app.get_data(Person, {'filters': [{'name': 'name', 'op': '==', 'val': 'sssxxx'}]})
    # objs = barracks_app.get_data(
    #     Computer, {'filters': [{'name': 'name', 'op': '==', 'val': 'lenovo'}]})
    # for obj in objs:
    #     print obj
    # barracks_app.mod_data(Person, {'filters': [{'name': 'name', 'op': '==', 'val': 'sssxxx'}]}, {
    #                       'birth_date': '2014-06-10', 'computers': {'add': [{'name': 'lenovo', 'vendor': 'ibm', 'purchase_time': '2015-04-09 00:00:01'}]}})
    barracks_app.create_api('test_api', ['GET'], test_api)
    barracks_app.run()
