# Blood Donation Application - Features & Details

This document provides a comprehensive overview of the functionality and technical details of the Blood Donation application.

## 🌟 Application Purpose
The platform connects blood donors with individuals, hospitals, and medical clinics in need of urgent blood donations, facilitating a streamlined and responsive emergency response system.

---

## 🚀 Core Features

### 1. User Authentication & Profile
- **Seamless Registration:** Integrated registration flow that creates a system user account and a linked `DonorProfile` simultaneously.
- **Login/Logout:** Secure authentication for users to manage their profiles and requests.
- **Profile Dashboard:** A dedicated space for authenticated users to:
    - View and update donor details (Blood Group, Phone, City, Address, Availability).
    - Update personal information (First Name, Last Name, Email).
    - Manage personal submitted blood requests (viewing and updating status).

### 2. Blood Request Management
- **Request Submission:** Authenticated users can post urgent blood requests. The system automatically populates contact information if a donor profile exists.
- **Request Feed:** A searchable and filterable feed of blood requests.
- **Advanced Filtering:**
    - By Blood Group.
    - By Urgency Level (Critical, Urgent, Standard).
    - By Location (City/Hospital).
    - By Status (Active vs. Fulfilled).
    - By Timeframe (Last 24h, Last 3 days).
- **Request Details:** Dedicated page for each request displaying full details, including contact information.
- **Request Fulfillment:** Creators can toggle the status of their requests (Active/Fulfilled) to keep the platform updated.
- **Donor Matching:** Displays matching available donors directly on the request detail page.

### 3. Donor Directory
- **Searchable Database:** A comprehensive list of registered donors.
- **Advanced Filtering:**
    - By Blood Group.
    - By City.
    - By Availability (Available Only).
- **Detailed Donor Profiles:** Public view of donor profiles, highlighting their availability and donation history.

### 4. Admin Dashboard
- **Management:** Administrators can manage all users, donor profiles, and blood requests via the Django Admin interface.

---

## 🛠️ Data Model Highlights

### BloodGroup
An enumeration defining the supported blood groups (A±, B±, O±, AB±).

### UrgencyLevel
An enumeration defining request urgency:
- **CRITICAL:** Within hours.
- **URGENT:** Within 24 hours.
- **STANDARD:** Within 2-3 days.

### DonorProfile Logic
- **Availability Toggle:** Users can set their own availability status.
- **Eligibility Tracking:** Includes built-in properties:
    - `is_eligible_to_donate`: Calculates eligibility (90 days after last whole blood donation).
    - `days_until_eligible`: Calculates remaining days until the donor can donate again.
- **Sorting:** Default sorting prioritizes available donors, total donations, and then by name.

### BloodRequest Logic
- **Tracking:** Stores requester, patient name, blood group, hospital, location, and urgency.
- **Ordering:** Default ordering prioritizes active requests followed by chronological creation time.
