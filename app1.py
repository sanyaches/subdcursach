from flask import Flask, render_template, request, session, copy_current_request_context
from DBcm import UseDataBase, ConnectionError, CredentialError, SQLError

app1 = Flask(__name__)

app1.config['dbconfig'] = {'host': '127.0.0.1',
                'user': 'root',
                'password': '228sanya228',
                'database': 'subdbd', }


@app1.route('/')
@app1.route('/main')
def main():
    return render_template('start.html', )


@app1.route('/regions')
def regions():
    try:
        with UseDataBase(app1.config['dbconfig']) as cursor:
            _SQL = """select id, region_name
                      from firm_region"""
            cursor.execute(_SQL)
            contents = cursor.fetchall()
        titles = ('ID', 'Регион')
        return render_template('regions.html',
                               the_title='Регионы',
                               row_titles=titles,
                               the_data=contents, )
    except ConnectionError as err:
        print('Trouble with SQL-server', str(err))
    except CredentialError as err:
        print('User-id/Password issues. Error:', str(err))
    except SQLError as err:
        print('Is your query correct? Error: ', str(err))
    except Exception as err:
        print('Something went wrong:', str(err))
    return 'Error'


@app1.route('/firm')
def firms():
    try:
        with UseDataBase(app1.config['dbconfig']) as cursor:
            _SQL = """select id, id_region, firm_name, firm_info
                      from firm"""      # CHANGEEEE for id_reg = name_reg
            cursor.execute(_SQL)
            contents = cursor.fetchall()
        titles = ('ID', 'Регион', 'Название фирмы', 'Информация')
        return render_template('firm.html',
                               the_title='Фирмы',
                               row_titles=titles,
                               the_data=contents, )
    except ConnectionError as err:
        print('Trouble with SQL-server', str(err))
    except CredentialError as err:
        print('User-id/Password issues. Error:', str(err))
    except SQLError as err:
        print('Is your query correct? Error: ', str(err))
    except Exception as err:
        print('Something went wrong:', str(err))
    return 'Error'


@app1.route('/firmservice')
def firmservice():
    try:
        with UseDataBase(app1.config['dbconfig']) as cursor:
            _SQL = """select id_firm, id_service
                      from firm_service"""      # CHANGEEEE
                                        # for id_firm(service) = firm_name
            cursor.execute(_SQL)
            contents = cursor.fetchall()
        titles = ('Фирма', 'Услуга')
        return render_template('firmservice.html',
                               the_title='Услуги фирм',
                               row_titles=titles,
                               the_data=contents, )
    except ConnectionError as err:
        print('Trouble with SQL-server', str(err))
    except CredentialError as err:
        print('User-id/Password issues. Error:', str(err))
    except SQLError as err:
        print('Is your query correct? Error: ', str(err))
    except Exception as err:
        print('Something went wrong:', str(err))
    return 'Error'


@app1.route('/services')
def services():
    try:
        with UseDataBase(app1.config['dbconfig']) as cursor:
            _SQL = """select id, service_name
                      from services"""
            cursor.execute(_SQL)
            contents = cursor.fetchall()
        titles = ('ID услуги', 'Услуга')
        return render_template('services.html',
                               the_title='Услуги',
                               row_titles=titles,
                               the_data=contents, )
    except ConnectionError as err:
        print('Trouble with SQL-server', str(err))
    except CredentialError as err:
        print('User-id/Password issues. Error:', str(err))
    except SQLError as err:
        print('Is your query correct? Error: ', str(err))
    except Exception as err:
        print('Something went wrong:', str(err))
    return 'Error'


################
#  ADD REGION  #
################
@app1.route('/addreg')
def show_addreg():
    return render_template('addreg.html')


@app1.route('/regions', methods=['POST'])
def addregion():
    with UseDataBase(app1.config['dbconfig']) as cursor:
        _SQL = """insert into firm_region
                    (id, region_name)
                    values 
                    (%s, %s)"""
        cursor.execute(_SQL, (request.form['id_reg'],
                              request.form['name_reg'],
                             ))
    return regions()


################
#   ADD FIRM   #
################
@app1.route('/addfirm')
def show_addfirm():
    return render_template('addfirm.html')


@app1.route('/firm', methods=['POST'])
def addfirm():
    with UseDataBase(app1.config['dbconfig']) as cursor:
        _SQL = """insert into firm
                    (id, id_region, firm_name, firm_info)
                    values 
                    (%s, %s, %s, %s)"""
        cursor.execute(_SQL, (request.form['id_firm'],
                              request.form['id_region'],
                              request.form['firm_name'],
                              request.form['firm_info'],
                             ))
    return firms()


########################
#   ADD FIRM SERVICE   #
########################
@app1.route('/addfirmservice')
def show_addfirmservice():
    return render_template('addfirmservice.html')


@app1.route('/firmservice', methods=['POST'])
def addfirmservice():
    with UseDataBase(app1.config['dbconfig']) as cursor:
        _SQL = """insert into firm_service
                    (id_firm, id_service)
                    values 
                    (%s, %s)"""
        cursor.execute(_SQL, (request.form['id_firm'],
                              request.form['id_service'],
                             ))
    return firmservice()


########################
#   ADD SERVICE   #
########################
@app1.route('/addservices')
def show_addservices():
    return render_template('addservices.html')


@app1.route('/services', methods=['POST'])
def addservices():
    with UseDataBase(app1.config['dbconfig']) as cursor:
        _SQL = """insert into services
                    (id, service_name)
                    values 
                    (%s, %s)"""
        cursor.execute(_SQL, (request.form['id_service'],
                              request.form['service_name'],
                             ))
    return services()


########################
#    DELETE REGION     #
########################
@app1.route('/chooseid')
def show_choose_id():
    return render_template('chooseid.html')


@app1.route('/delregions', methods=['POST'])
def show_delregion():
    with UseDataBase(app1.config['dbconfig']) as cursor:
        _SQL = """delete from firm_region where id=%(my_id)s"""
        cursor.execute(_SQL, {'my_id': request.form['id_edit_del']})
    return regions()


########################
#    DELETE FIRM       #
########################
@app1.route('/chooseidfirm')
def show_choose_id_firm():
    return render_template('chooseidfirm.html')


@app1.route('/delfirm', methods=['POST'])
def show_delfirm():
    with UseDataBase(app1.config['dbconfig']) as cursor:
        _SQL = """delete from firm where id=%(my_id)s"""
        cursor.execute(_SQL, {'my_id': request.form['id_edit_del']})
    return firms()


########################
#  DELETE FIRMSERVICE  #
########################
@app1.route('/chooseidfirmservice')
def show_choose_id_firmservice():
    return render_template('chooseidfirmservice.html')


@app1.route('/delfirmservice', methods=['POST'])
def show_delfirmservice():
    with UseDataBase(app1.config['dbconfig']) as cursor:
        _SQL = """delete from firm_service where id_firm=%(my_id_firm)s and id_service=%(my_id_service)s"""
        cursor.execute(_SQL, {'my_id_firm': request.form['id_edit_del_firm'],
                              'my_id_service': request.form['id_edit_del_service']
                              })
    return firmservice()


########################
#  DELETE SERVICE      #
########################
@app1.route('/chooseidservice')
def show_choose_id_service():
    return render_template('chooseidservice.html')


@app1.route('/delservice', methods=['POST'])
def show_delservice():
    with UseDataBase(app1.config['dbconfig']) as cursor:
        _SQL = """delete from services where id=%(my_id)s"""
        cursor.execute(_SQL, {'my_id': request.form['id_edit_del']})

    return services()


########################
#      EDIT REGION     #
########################
@app1.route('/editregion')
def show_chooseregion():
    return render_template('chooseidedit.html',
                           )


@app1.route('/editregions', methods=['POST'])
def show_editregion():
    with UseDataBase(app1.config['dbconfig']) as cursor:
        _SQL = """select * from firm_region where id=%(my_id)s"""
        cursor.execute(_SQL, {'my_id': request.form['id_edit_del']})
        contents = cursor.fetchall()
    return render_template('editreg.html',
                           id_reg=contents[0][0],
                           reg_name=contents[0][1]
                           )


@app1.route('/editedregions', methods=['POST'])
def show_editedregion():
    with UseDataBase(app1.config['dbconfig']) as cursor:
        _SQL = """update firm_region set region_name=%(my_name)s where id=%(my_id)s"""
        cursor.execute(_SQL, {'my_id': request.form['id_reg'],
                              'my_name': request.form['name_reg']})
    return regions()




########################
#      EDIT FIRM       #
########################
@app1.route('/editfirm')
def show_choosefirm():
    return render_template('chooseideditfirm.html',
                           )


@app1.route('/editfirms', methods=['POST'])
def show_editfirm():
    with UseDataBase(app1.config['dbconfig']) as cursor:
        _SQL = """select * from firm where id=%(my_id)s"""
        cursor.execute(_SQL, {'my_id': request.form['id_edit_del']})
        contents = cursor.fetchall()
    return render_template('editfirm.html',
                           id_firm=contents[0][0],
                           id_reg=contents[0][1],
                           firm_name=contents[0][2],
                           firm_info=contents[0][3]
                           )


@app1.route('/editedfirms', methods=['POST'])
def show_editedfirm():
    with UseDataBase(app1.config['dbconfig']) as cursor:
        _SQL = """update firm
                  set id_region=%(my_id_reg)s, firm_name=%(my_name)s, firm_info=%(my_info)s
                  where id=%(my_id)s"""
        cursor.execute(_SQL, {'my_id': request.form['id'],
                              'my_id_reg': request.form['id_reg'],
                              'my_info': request.form['info_firm'],
                              'my_name': request.form['name_firm']})
    return firms()


########################
#    EDIT SERVICES     #
########################
@app1.route('/editservice')
def show_chooseservice():
    return render_template('chooseideditservice.html',
                           )


@app1.route('/editservices', methods=['POST'])
def show_editservice():
    with UseDataBase(app1.config['dbconfig']) as cursor:
        _SQL = """select * from services where id=%(my_id)s"""
        cursor.execute(_SQL, {'my_id': request.form['id_edit_del']})
        contents = cursor.fetchall()
    return render_template('editservice.html',
                           id_service=contents[0][0],
                           name_service=contents[0][1],
                           )


@app1.route('/editedservices', methods=['POST'])
def show_editedservice():
    with UseDataBase(app1.config['dbconfig']) as cursor:
        _SQL = """update services
                  set service_name=%(my_name)s
                  where id=%(my_id)s"""
        cursor.execute(_SQL, {'my_id': request.form['id_service'],
                              'my_name': request.form['name_service']})
    return services()


########################
#       SEARCHING      #
########################
@app1.route('/searching')
def searching():
    return render_template('search.html',
                           )


@app1.route('/searched', methods=['POST'])
def searched():
    with UseDataBase(app1.config['dbconfig']) as cursor:
        _SQL1 = """select id 
                  from firm_region 
                  where region_name=%(reg_name)s"""
        cursor.execute(_SQL1, {'reg_name': request.form['reg_name']})
        contents = cursor.fetchall()
        id_reg = contents[0][0]

        _SQL2 = """select id 
                   from services 
                   where service_name=%(serv_name)s"""
        cursor.execute(_SQL2, {'serv_name': request.form['service_name']})
        contents = cursor.fetchall()
        id_serv = contents[0][0]

        _SQL = """select * 
                  from firm f, firm_region r, firm_service fs 
                  where f.id_region=%(id_reg)s and fs.id_service=%(id_serv)s 
                  and r.id=f.id_region and fs.id_firm=f.id"""
        cursor.execute(_SQL, {'id_serv': str(id_serv), 'id_reg': str(id_reg)})
        contents = cursor.fetchall()
        edited_conents = []
        for row in contents:
            add = []
            add.append(row[2])
            add.append(request.form['reg_name'])
            add.append(request.form['service_name'])
            add.append(row[3])
            edited_conents.append(add)

    titles = ('Название фирмы', 'Регион', 'Услуга', 'Информация о фирме')
    return render_template('searched.html',
                           the_title='Найденные фирмы',
                           row_titles=titles,
                           the_data=edited_conents, )


if __name__ == '__main__':
    app1.run()
