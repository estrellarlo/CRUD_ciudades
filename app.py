from flask import Flask, request, render_template, redirect, url_for, flash
import pyodbc

app = Flask(__name__)
app.secret_key = 'supersecretkey'  

#Conexión bd
def get_db_connection():
    conn = pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=LENOVO_ARLO\\SQLEXPRESS01;"
        "DATABASE=Estados;"
        "Trusted_Connection=yes;"
    )
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM ciudades ORDER BY id")
    ciudades = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('index.html', ciudades=ciudades)

@app.route('/view/<int:id>')
def view_city(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM ciudades WHERE id = ?", (id,))
    ciudad = cursor.fetchone()
    cursor.close()
    conn.close()
    return render_template('view_city.html', ciudad=ciudad)

@app.route('/add', methods=['GET', 'POST'])
def add_city():
    if request.method == 'POST':
        id = request.form['id']
        nombre = request.form['nombre']
        poblacion = int(request.form['poblacion'])
        fecha_fundacion = request.form['fecha_fundacion']
        historia = request.form['historia']
        
        conn = get_db_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("""
                INSERT INTO ciudades (id, nombre, poblacion, Fecha_fundacion, Historia)
                VALUES (?, ?, ?, ?, ?)
            """, (id, nombre, poblacion, fecha_fundacion, historia))
            conn.commit()
        except pyodbc.IntegrityError:
            conn.rollback()
            flash('Error al añadir ciudad: el ID ya existe.')
            return redirect(url_for('add_city'))
        finally:
            cursor.close()
            conn.close()
        
        return redirect(url_for('index'))
    
    return render_template('add_city.html')


@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_city(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    if request.method == 'POST':
        nombre = request.form['nombre']
        poblacion = int(request.form['poblacion'])
        fecha_fundacion = request.form['fecha_fundacion']
        historia = request.form['historia']
        cursor.execute("""
            UPDATE ciudades
            SET nombre = ?, poblacion = ?, Fecha_fundacion = ?, Historia = ?
            WHERE id = ?
        """, (nombre, poblacion, fecha_fundacion, historia, id))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('index'))
    cursor.execute("SELECT * FROM ciudades WHERE id = ?", (id,))
    ciudad = cursor.fetchone()
    cursor.close()
    conn.close()
    return render_template('edit_city.html', ciudad=ciudad)

@app.route('/delete/<int:id>', methods=['POST'])
def delete_city(id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM empresas WHERE id_ciudad = ?", (id,))
        cursor.execute("DELETE FROM ciudades WHERE id = ?", (id,))
        conn.commit()
        cursor.close()
        conn.close()
        flash('Ciudad eliminada exitosamente.')
    except pyodbc.IntegrityError:
        flash('No se puede eliminar esta ciudad porque está siendo referenciada en otra tabla.')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
