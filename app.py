from flask import Flask, render_template, request

app = Flask(__name__)

doctors = []
patients = []

def load_doctors():
    # Load the doctor details from the doctor.txt file
    with open('doctor.txt', 'r') as file:
        lines = file.readlines()

    doctors_list = []

    for line in lines:
        details = line.strip().split(',')
        id = details[0].split(' | ')[1].strip()
        name = details[1].split(' | ')[1].strip()
        age = details[2].split(' | ')[1].strip()
        gender = details[3].split(' | ')[1].strip()
        specialization = details[4].split(' | ')[1].strip()
        shift_time = details[5].split(' | ')[1].strip()
        password = details[6].split(' | ')[1].strip()

        doctor = {
            'id': id,
            'name': name,
            'age': age,
            'gender': gender,
            'specialization': specialization,
            'shift_time': shift_time,
            'password': password
        }

        doctors_list.append(doctor)

    return doctors_list


def load_patients():
    # Load the patient details from the patient.txt file
    with open('patient.txt', 'r') as file:
        lines = file.readlines()

    patients_list = []

    for line in lines:
        details = line.strip().split(',')
        id = details[0].split(' | ')[1].strip()
        name = details[1].split(' | ')[1].strip()
        age = details[2].split(' | ')[1].strip()
        gender = details[3].split(' | ')[1].strip()
        doctor_id = details[4].split(' | ')[1].strip()
        appointment_time = details[5].split(' | ')[1].strip()
        password = details[6].split(' | ')[1].strip()

        patient = {
            'id': id,
            'name': name,
            'age': age,
            'gender': gender,
            'doctor_id': doctor_id,
            'appointment_time': appointment_time,
            'password': password
        }

        patients_list.append(patient)

    return patients_list


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        hospital_choice = request.form.get('hospital_choice')
        if hospital_choice == '0':
            return 'Exiting the program...'
        elif hospital_choice in ['1', '2', '3']:
            if hospital_choice == '1':
                hospital_name = 'Apollo Hospital'
            elif hospital_choice == '2':
                hospital_name = 'LifeCare Hospital'
            else:
                hospital_name = 'Manipal Hospital'
            return render_template('menu.html', hospital_name=hospital_name)
    return render_template('index.html')


@app.route('/menu/<hospital_name>', methods=['GET', 'POST'])
def menu(hospital_name):
    if request.method == 'POST':
        choice = request.form.get('choice')
        if choice == '1':
            return render_template('doctor.html', hospital_name=hospital_name)
        elif choice == '2':
            return render_template('patient.html', hospital_name=hospital_name)
        elif choice == '3':
            return render_template('index.html')
    return render_template('menu.html', hospital_name=hospital_name)


@app.route('/doctor_menu/<hospital_name>', methods=['GET', 'POST'])
def doctor_menu(hospital_name):
    if request.method == 'POST':
        choice = request.form.get('choice')
        if choice == '1':
            return render_template('doctor_signup.html', hospital_name=hospital_name)
        elif choice == '2':
            return render_template('doctor_login.html', hospital_name=hospital_name)
        elif choice == '3':
            return render_template('index.html')
    doctors = load_doctors()
    return render_template('doctor_menu.html', hospital_name=hospital_name, doctors=doctors)


@app.route('/doctor_signup/<hospital_name>', methods=['POST'])
def doctor_signup(hospital_name):
    if request.method == 'POST':
        name = request.form.get('name')
        age = request.form.get('age')
        gender = request.form.get('gender')
        specialization = request.form.get('specialization')
        shift_time = request.form.get('shift_time')
        password = request.form.get('password')

        # Generate a unique ID for the doctor
        doctor_id = 'D' + str(len(doctors) + 1)

        # Create a new Doctor object
        doctor = {
            'id': doctor_id,
            'name': name,
            'age': age,
            'gender': gender,
            'specialization': specialization,
            'shift_time': shift_time,
            'password': password
        }

        # Append the doctor to the 'doctors' list
        doctors.append(doctor)

        # Save the doctor details to the doctor.txt file
        with open('doctor.txt', 'a') as file:
            file.write(f"ID | {doctor_id}, Name | {name}, Age | {age}, Gender | {gender}, "
                       f"Specialization | {specialization}, Shift Time | {shift_time}, Password | {password}\n")

        return f'Doctor sign up successful! ID: {doctor_id}'

    return render_template('doctor.html', hospital_name=hospital_name)



@app.route('/doctor_login/<hospital_name>', methods=['POST'])
def doctor_login(hospital_name):
    if request.method == 'POST':
        id = request.form.get('id')
        password = request.form.get('password')

        # Check if the doctor credentials match
        for doctor in doctors:
            if doctor['id'] == id and doctor['password'] == password:
                patients_list = [patient for patient in patients if patient['doctor_id'] == id]
                return render_template('doctor_dashboard.html', hospital_name=hospital_name, doctor=doctor,
                                       patients=patients_list)

        return 'Invalid doctor credentials'

    return render_template('doctor.html', hospital_name=hospital_name)


@app.route('/patient_menu/<hospital_name>', methods=['GET', 'POST'])
def patient_menu(hospital_name):
    if request.method == 'POST':
        choice = request.form.get('choice')
        if choice == '1':
            doctors = load_doctors()
            return render_template('patient_signup.html', hospital_name=hospital_name, doctors=doctors)
        elif choice == '2':
            return render_template('patient_login.html', hospital_name=hospital_name)
        elif choice == '3':
            return render_template('index.html')
    return render_template('patient_menu.html', hospital_name=hospital_name)


@app.route('/patient_signup/<hospital_name>', methods=['POST'])
def patient_signup(hospital_name):
    if request.method == 'POST':
        name = request.form.get('name')
        age = request.form.get('age')
        gender = request.form.get('gender')
        doctor_id = request.form.get('doctor_id')
        appointment_time = request.form.get('appointment_time')
        password = request.form.get('password')

        # Generate a unique ID for the patient
        patient_id = 'P' + str(len(patients) + 1)

        # Create a new Patient object
        patient = {
            'id': patient_id,

            'name': name,
            'age': age,
            'gender': gender,
            'doctor_id': doctor_id,
            'appointment_time': appointment_time,
            'password': password
        }

        # Append the patient to the 'patients' list
        patients.append(patient)

        # Save the patient details to the patient.txt file
        with open('patient.txt', 'a') as file:
            file.write(f"ID | {patient_id}, Name | {name}, Age | {age}, Gender | {gender}, "
                       f"Doctor ID | {doctor_id}, Appointment Time | {appointment_time}, Password | {password}\n")

        return f'Patient sign up successful! ID: {patient_id}'

    return render_template('patient.html', hospital_name=hospital_name)


@app.route('/patient_login/<hospital_name>', methods=['POST'])
def patient_login(hospital_name):
    if request.method == 'POST':
        id = request.form.get('id')
        password = request.form.get('password')

        # Check if the patient credentials match
        for patient in patients:
            if patient['id'] == id and patient['password'] == password:
                doctor_id = patient['doctor_id']
                doctor = next((doctor for doctor in doctors if doctor['id'] == doctor_id), None)
                return render_template('patient_dashboard.html', hospital_name=hospital_name, patient=patient,
                                       doctor=doctor)

        return 'Invalid patient credentials'

    return render_template('patient.html', hospital_name=hospital_name)


if __name__ == '__main__':
    app.run()
