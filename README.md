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

- Add a doctor profile:
  <domain_name>/register/doctor/

- Add a patient profile:
  <domain_name>/register/patient/

- Create an appointment:
  <domain_name>/create/appointment/<user_id>/

- Create unavailable time:
  <domain_name>/register/appointment/unavailable/<user_id>/
