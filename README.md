# telemedicine_app

**What It Is**

A simple application that allows users register as doctors or patients.

Patients can make appointments with doctors as long as its within the doctors available time.

Doctors can set their unavailable time, there are checks to ensure no overlaps.




**Limitations**

- No authentication scheme on the backend, supported request methods are only post.
- Testing should not be from a browser because of cors restrictions.




**End Points**

- Register new User:
  <domain_name>/register/

  *post data fields:*

  - email
  - password
  - is_doctor: boolean

- Add a doctor profile:
  <domain_name>/register/doctor/

  *post data fields:*

  - user: int (user id)
  - first_name
  - last_name
  - age
  - gender ("male" or "female")

- Add a patient profile:
  <domain_name>/register/patient/

  *post data fields:*

  - user: int (user id)
  - first_name
  - last_name
  - age
  - gender ("male" or "female" or "other")

- Create an appointment:
  <domain_name>/create/appointment/<user_id>/

  *post data fields:*

  - start_time: Unix DateTime format
  - end_time: Unix DateTime format
  - doctor: int(doctor_id)
  - patient: int(patient_id)

- Create unavailable time:
  <domain_name>/create/appointment/unavailable/<user_id>/

  *post data fields:*

  - start_time: Unix DateTime format
  - end_time: Unix DateTime format
  - doctor: int(doctor_id)
