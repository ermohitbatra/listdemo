import streamlit as st
import requests
import json
import uuid
import streamlit_extras
from streamlit_extras.switch_page_button import switch_page

def send_request(filename):
    api_url = "https://relevate-dev-7eg829ox.uc.gateway.dev/fileschema?key=AIzaSyCZtchZF_nqmzY_tnaN25De2IutsN3zld0"
    payload = {"fileName": filename}
    headers = {'Content-Type': 'application/json'}

    try:
        response = requests.post(api_url, data=json.dumps(payload), headers=headers)
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

def send_request_api2(filename, response_api1, list_type, space_id, primary_id):
    api_url2 = "https://relevate-dev-7eg829ox.uc.gateway.dev/list?key=AIzaSyCZtchZF_nqmzY_tnaN25De2IutsN3zld0"

    file_schema = response_api1 if isinstance(response_api1, list) else response_api1.get("fileSchema", [])

    payload = {
        "listType": list_type,
        "spaceId": space_id,
        "columnMap": {"primaryId": primary_id},
        "fileSchema": file_schema,
        "computedColumns": [],
        "listMappings": [
            {
                "list": "RelevateContact",
                "mappings": [
                    {"listColumn": "FIRSTNAME", "fileColumn": "{{column.Firstname}}"},
                    {"listColumn": "LASTNAME", "fileColumn": "{{column.Lastname}}"},
                    {"listColumn": "ADDRESS_1", "fileColumn": "{{column.Address1}}"},
                    {"listColumn": "ADDRESS_2", "fileColumn": "{{column.Address2}}"},
                    {"listColumn": "CITY", "fileColumn": "{{column.City}}"},
                    {"listColumn": "STATE", "fileColumn": "{{column.STATE}}"},
                    {"listColumn": "ZIP", "fileColumn": "{{column.Zip}}"},
                    {"listColumn": "EMAIL", "fileColumn": "{{column.Email}}"},
                    {"listColumn": "PHONE", "fileColumn": "{{column.Phone}}"},
                    {"listColumn": "Age", "fileColumn": "{{column.Age}}"},
                    {"listColumn": "Gender", "fileColumn": "{{column.Gender}}"},
                    {"listColumn": "Income", "fileColumn": "{{column.Income}}"},
                    {"listColumn": "Education", "fileColumn": "{{column.Education}}"}
                ]
            }
        ]
    }

    headers = {'Content-Type': 'application/json'}

    try:
        response = requests.post(api_url2, data=json.dumps(payload), headers=headers)
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

def get_api_response(uuid):
    api_url3 = f"https://relevate-dev-7eg829ox.uc.gateway.dev/list/uuid/details?key=AIzaSyCZtchZF_nqmzY_tnaN25De2IutsN3zld0&uuid={uuid}"
    try:
        response = requests.get(api_url3)
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

def get_api_response2(uuid):
    api_url4 = f"https://getdatavaultstatus-580005102993.us-central1.run.app?uuid={uuid}"
    try:
        response = requests.get(api_url4)
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

if "page" not in st.session_state:
    st.session_state.page = "home"

# First Page
if st.session_state.page == "home":
    # Streamlit UI
    st.title("LIST Request App")

    logId = str(uuid.uuid1())

    filename = st.text_input("Enter Filename (e.g., Filename.csv)")
    list_type = f"{filename}-{logId}"
    list_type = list_type.replace('.csv','')
    space_id = "123456"
    primary_id = "{{column.PatientId}}"

    if filename:
        st.write(f"**Entered File:** {filename}")

        if st.button("Send Request"):
            response_api1 = send_request(filename)
            # st.write("### Response from API1:")
            # st.json(response_api1)

            response_api2 = send_request_api2(filename, response_api1, list_type, space_id, primary_id)
            st.write("### Response:")
            st.json(response_api2)

            if "uuid" in response_api2:
                st.session_state.api_uuid = response_api2["uuid"]

        if st.button("Fetch Data from GET API (List)") and "api_uuid" in st.session_state:
            response_api3 = get_api_response(st.session_state.api_uuid)
            st.write("### Response from GET API:")
            st.json(response_api3)

        if st.button("Fetch Data from GET API (Entity Resolution)") and "api_uuid" in st.session_state:
            response_api4 = get_api_response2(st.session_state.api_uuid)
            st.write("### Response from GET API:")
            st.json(response_api4)

    # Create a hyperlink-like button to navigate
    if st.button("Report"):
        st.session_state.page = "second"
        st.rerun()

    # Second Page
elif st.session_state.page == "second":
    st.title("Second Page")
    st.write("Welcome to the second page!")

    # Option to go back
    if st.button("Back to Home"):
        st.session_state.page = "home"
        st.rerun()
    
    st.markdown(
    f'<iframe title="EntityResolutionData" width="1000" height="500" src="https://app.powerbi.com/view?r=eyJrIjoiMjE0ODY5MmYtMDE4MS00Y2E1LTg4ZTAtODI0OWQyOGEyYzRjIiwidCI6IjFmMmI1ZGU5LWU5ZGQtNDE5YS1hZGU1LWZlZTZjOTJlN2Y5MiIsImMiOjN9" frameborder="0" allowFullScreen="true"></iframe>',
    unsafe_allow_html=True
    )