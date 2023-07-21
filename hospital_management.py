import streamlit as st
import xml.etree.ElementTree as ET


def search_patient():
    # Load the XML file content
    with open('hospital_management.xml', 'r') as file:
        xml_content = file.read()

    # Parse the XML content
    root = ET.fromstring(xml_content)

    # Create input field for patient name
    search_name = st.text_input("Name")

    # Create a button to search for the patient
    if st.button("Search"):
        if search_name:
            # Search for the patient element with the given name
            patient_found = False
            for patient in root.findall('Patients/patient'):
                fname_element = patient.find('Name/fname')
                if fname_element is not None and fname_element.text is not None:
                    fname = fname_element.text
                    if fname.lower() == search_name.lower():
                        patient_found = True

                        # Display patient information
                        st.write("Patient Name:", fname)
                        st.write("SSN:", patient.find('SSN').text)
                        st.write("Age:", patient.find('age').text)
                        st.write("Room No:", patient.find('roomno').text)
                        st.write("Medical Problem:", patient.find(
                            'Medicalproblem').text)
                        st.write("Drug Allergy:", patient.find(
                            'Drugallergy').text)
                        st.write("Primary Insurance ID:", patient.find(
                            'Insurance[@type="Primary"]/P.id').text)
                        st.write("Primary Insurance Address:", patient.find(
                            'Insurance[@type="Primary"]/P.address').text)
                        st.write("Secondary Insurance ID:", patient.find(
                            'Insurance[@type="Secondary"]/S.id').text)
                        st.write("Secondary Insurance Address:", patient.find(
                            'Insurance[@type="Secondary"]/S.address').text)

                        break

            if not patient_found:
                st.write("Patient not found.")
        else:
            st.write("Please enter a patient name.")


def add_patient():
    # Create input fields for patient information
    fname = st.text_input("First Name")
    mname = st.text_input("Middle Name")
    lname = st.text_input("Last Name")
    ssn = st.text_input("SSN")
    age = st.text_input("Age")
    roomno = st.text_input("Room No")
    primary_insurance_id = st.text_input("Primary Insurance ID")
    primary_insurance_address = st.text_input("Primary Insurance Address")
    secondary_insurance_id = st.text_input("Secondary Insurance ID")
    secondary_insurance_address = st.text_input("Secondary Insurance Address")
    medical_problem = st.text_input("Medical Problem")
    drug_allergy = st.text_input("Drug Allergy")

    if fname and mname and lname and ssn and age and roomno and primary_insurance_id and primary_insurance_address and secondary_insurance_id and secondary_insurance_address and medical_problem and drug_allergy:
        # Load the XML file content
        tree = ET.parse('hospital_management.xml')
        root = tree.getroot()

        # Check if the patient already exists
        patient_found = False
        for patient in root.findall('Patients/patient'):
            fname_element = patient.find('Name/fname')
            ssn_element = patient.find('SSN')
            if fname_element is not None and fname_element.text is not None and ssn_element is not None and ssn_element.text is not None:
                if fname_element.text.lower() == fname.lower() and ssn_element.text == ssn:
                    patient_found = True
                    st.write("Patient with the same name and SSN already exists.")
                    break

        if not patient_found:
            # Create patient element
            patient = ET.Element('patient')

            # Create name element
            name = ET.SubElement(patient, 'Name')
            fname_elem = ET.SubElement(name, 'fname')
            fname_elem.text = fname
            mname_elem = ET.SubElement(name, 'mname')
            mname_elem.text = mname
            lname_elem = ET.SubElement(name, 'lname')
            lname_elem.text = lname

            # Create SSN element
            ssn_elem = ET.SubElement(patient, 'SSN')
            ssn_elem.text = ssn

            # Create age element
            age_elem = ET.SubElement(patient, 'age')
            age_elem.text = age

            # Create roomno element
            roomno_elem = ET.SubElement(patient, 'roomno')
            roomno_elem.text = roomno

            # Create primary insurance element
            primary_insurance = ET.SubElement(
                patient, 'Insurance', type="Primary")
            primary_id_elem = ET.SubElement(primary_insurance, 'P.id')
            primary_id_elem.text = primary_insurance_id
            primary_address_elem = ET.SubElement(
                primary_insurance, 'P.address')
            primary_address_elem.text = primary_insurance_address

            # Create secondary insurance element
            secondary_insurance = ET.SubElement(
                patient, 'Insurance', type="Secondary")
            secondary_id_elem = ET.SubElement(secondary_insurance, 'S.id')
            secondary_id_elem.text = secondary_insurance_id
            secondary_address_elem = ET.SubElement(
                secondary_insurance, 'S.address')
            secondary_address_elem.text = secondary_insurance_address

            # Create medical problem element
            medical_problem_elem = ET.SubElement(patient, 'Medicalproblem')
            medical_problem_elem.text = medical_problem

            # Create drug allergy element
            drug_allergy_elem = ET.SubElement(patient, 'Drugallergy')
            drug_allergy_elem.text = drug_allergy

            # Append patient element to root
            root.find('Patients').append(patient)

            # Write the changes back to the XML file
            tree.write('hospital_management.xml')

            # Display success message
            st.success("Patient '{}' added successfully.".format(fname))
    else:
        st.write("Please fill in all the required fields.")


def delete_patient():
    # Load the XML file content
    tree = ET.parse('hospital_management.xml')
    root = tree.getroot()

    # Create input field for patient name
    delete_name = st.text_input("Name")

    # Create a button to confirm deletion
    if st.button("Confirm"):
        if delete_name:
            # Search for the patient element with the given name
            patient_found = False
            for patient in root.findall('Patients/patient'):
                fname_element = patient.find('Name/fname')
                if fname_element is not None and fname_element.text is not None:
                    fname = fname_element.text
                    if fname.lower() == delete_name.lower():
                        patient_found = True

                        # Remove the patient element from the root
                        root.find('Patients').remove(patient)

                        # Write the changes back to the XML file
                        tree.write('hospital_management.xml')

                        # Display success message
                        st.success("Patient '{}' deleted.".format(fname))

                        break

            if not patient_found:
                st.warning(
                    "No patient found with the name '{}'.".format(delete_name))
        else:
            st.write("Please enter a patient name.")


def main():
    st.title("Hospital Management System")

    # Create sidebar menu
    menu = ["Search Patient", "Add Patient", "Delete Patient"]
    choice = st.sidebar.selectbox("Menu", menu)

    # Display the selected menu
    if choice == "Search Patient":
        search_patient()
    elif choice == "Add Patient":
        add_patient()
    elif choice == "Delete Patient":
        delete_patient()


if __name__ == "__main__":
    main()






