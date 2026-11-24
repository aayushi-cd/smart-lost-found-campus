import streamlit as st
import pandas as pd
from datetime import date

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------
st.set_page_config(
    page_title="Smart Lost & Found Campus System",
    page_icon="🔎",
    layout="wide"
)

# --------------------------------------------------
# SESSION DATA
# --------------------------------------------------
if "items" not in st.session_state:
    st.session_state["items"] = [
        {
            "ID": 1,
            "Name": "Samsung Phone",
            "Category": "Electronics",
            "Description": "Black Samsung smartphone with transparent cover",
            "Location": "University Cafeteria",
            "Date": "2026-11-20",
            "Type": "Lost",
            "Status": "Searching"
        },
        {
            "ID": 2,
            "Name": "Black Wallet",
            "Category": "Personal Item",
            "Description": "Black leather wallet containing student ID",
            "Location": "Library",
            "Date": "2026-11-21",
            "Type": "Found",
            "Status": "Available"
        },
        {
            "ID": 3,
            "Name": "Water Bottle",
            "Category": "Other",
            "Description": "Blue Milton water bottle",
            "Location": "Block C",
            "Date": "2026-11-22",
            "Type": "Found",
            "Status": "Available"
        },
        {
            "ID": 4,
            "Name": "College ID Card",
            "Category": "Documents",
            "Description": "Student identification card",
            "Location": "Academic Block",
            "Date": "2026-11-23",
            "Type": "Lost",
            "Status": "Searching"
        }
    ]

if "claims" not in st.session_state:
    st.session_state.claims = [
        {
            "Claim ID": 101,
            "Item": "Black Wallet",
            "Claimant": "Student User",
            "Proof": "Can identify the cards inside the wallet",
            "Status": "Pending"
        }
    ]

if "notifications" not in st.session_state:
    st.session_state.notifications = [
        "A possible match was found for a recently reported item.",
        "Your lost item report has been successfully registered.",
        "Claim #101 is currently under administrator verification."
    ]


# --------------------------------------------------
# HELPER FUNCTIONS
# --------------------------------------------------
def add_item(name, category, description, location, item_date, item_type):
    new_id = max([item["ID"] for item in st.session_state["items"]], default=0) + 1

    status = "Searching" if item_type == "Lost" else "Available"

    st.session_state["items"].append(
        {
            "ID": new_id,
            "Name": name,
            "Category": category,
            "Description": description,
            "Location": location,
            "Date": str(item_date),
            "Type": item_type,
            "Status": status
        }
    )


def find_matches():
    lost_items = [
        item for item in st.session_state["items"]
        if item["Type"] == "Lost"
    ]

    found_items = [
        item for item in st.session_state["items"]
        if item["Type"] == "Found"
    ]

    matches = []

    for lost in lost_items:
        for found in found_items:

            score = 0

            if lost["Category"] == found["Category"]:
                score += 40

            if lost["Location"].lower() == found["Location"].lower():
                score += 30

            lost_words = set(lost["Name"].lower().split())
            found_words = set(found["Name"].lower().split())

            if lost_words.intersection(found_words):
                score += 30

            if score >= 40:
                matches.append({
                    "Lost Item": lost["Name"],
                    "Found Item": found["Name"],
                    "Location": found["Location"],
                    "Match Score": f"{score}%"
                })

    return matches


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------
st.sidebar.title("🔎 Smart Lost & Found")

st.sidebar.caption("Campus Recovery Management System")

page = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Dashboard",
        "🔴 Report Lost Item",
        "🟢 Report Found Item",
        "🔍 Search Items",
        "✨ Possible Matches",
        "📋 Claims",
        "🔔 Notifications",
        "🛡️ Admin Panel",
        "ℹ️ About Project"
    ]
)

st.sidebar.divider()

st.sidebar.write("**Project:** Smart Lost & Found")
st.sidebar.write("**Technology:** Java + OOAD + Streamlit")
st.sidebar.write("**Status:** Prototype")


# --------------------------------------------------
# DASHBOARD
# --------------------------------------------------
if page == "🏠 Dashboard":

    st.title("🔎 Smart Lost & Found Campus System")

    st.write(
        "A centralized campus platform for reporting, searching "
        "and recovering lost belongings."
    )

    st.divider()

    lost_count = len([
        x for x in st.session_state["items"]
        if x["Type"] == "Lost"
    ])

    found_count = len([
        x for x in st.session_state["items"]
        if x["Type"] == "Found"
    ])

    pending_claims = len([
        x for x in st.session_state.claims
        if x["Status"] == "Pending"
    ])

    recovered = len([
        x for x in st.session_state["items"]
        if x["Status"] == "Recovered"
    ])

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("🔴 Lost Items", lost_count)
    col2.metric("🟢 Found Items", found_count)
    col3.metric("📋 Pending Claims", pending_claims)
    col4.metric("✅ Recovered", recovered)

    st.subheader("Recent Reports")

    df = pd.DataFrame(st.session_state["items"])

    st.dataframe(
        df[["ID", "Name", "Category", "Location", "Type", "Status"]],
        use_container_width=True,
        hide_index=True
    )

    st.subheader("System Workflow")

    st.info(
        "Report Item  →  Search & Match  →  Submit Claim  →  "
        "Admin Verification  →  Item Returned"
    )


# --------------------------------------------------
# REPORT LOST ITEM
# --------------------------------------------------
elif page == "🔴 Report Lost Item":

    st.title("🔴 Report a Lost Item")

    st.write(
        "Provide information about the item you lost on campus."
    )

    with st.form("lost_form"):

        name = st.text_input("Item Name")

        category = st.selectbox(
            "Category",
            [
                "Electronics",
                "Documents",
                "Personal Item",
                "Books",
                "Keys",
                "Clothing",
                "Other"
            ]
        )

        description = st.text_area("Description")

        location = st.text_input("Location Lost")

        lost_date = st.date_input(
            "Date Lost",
            value=date.today()
        )

        submitted = st.form_submit_button(
            "Submit Lost Item Report",
            type="primary"
        )

        if submitted:

            if not name or not location:
                st.error(
                    "Please enter the item name and location."
                )

            else:
                add_item(
                    name,
                    category,
                    description,
                    location,
                    lost_date,
                    "Lost"
                )

                st.session_state.notifications.insert(
                    0,
                    f"Lost item '{name}' was successfully reported."
                )

                st.success(
                    "Lost item reported successfully!"
                )


# --------------------------------------------------
# REPORT FOUND ITEM
# --------------------------------------------------
elif page == "🟢 Report Found Item":

    st.title("🟢 Report a Found Item")

    st.write(
        "Help another student recover their belonging."
    )

    with st.form("found_form"):

        name = st.text_input("Item Name")

        category = st.selectbox(
            "Category",
            [
                "Electronics",
                "Documents",
                "Personal Item",
                "Books",
                "Keys",
                "Clothing",
                "Other"
            ]
        )

        description = st.text_area("Description")

        location = st.text_input("Location Found")

        found_date = st.date_input(
            "Date Found",
            value=date.today()
        )

        submitted = st.form_submit_button(
            "Submit Found Item Report",
            type="primary"
        )

        if submitted:

            if not name or not location:
                st.error(
                    "Please enter the item name and location."
                )

            else:

                add_item(
                    name,
                    category,
                    description,
                    location,
                    found_date,
                    "Found"
                )

                st.session_state.notifications.insert(
                    0,
                    f"Found item '{name}' was successfully registered."
                )

                st.success(
                    "Found item registered successfully!"
                )


# --------------------------------------------------
# SEARCH
# --------------------------------------------------
elif page == "🔍 Search Items":

    st.title("🔍 Search Lost & Found Items")

    search = st.text_input(
        "Search by item name, category or location"
    )

    item_type = st.selectbox(
        "Item Type",
        ["All", "Lost", "Found"]
    )

    df = pd.DataFrame(st.session_state["items"])

    if search:

        mask = (
            df["Name"].str.contains(
                search,
                case=False,
                na=False
            )
            |
            df["Category"].str.contains(
                search,
                case=False,
                na=False
            )
            |
            df["Location"].str.contains(
                search,
                case=False,
                na=False
            )
        )

        df = df[mask]

    if item_type != "All":
        df = df[df["Type"] == item_type]

    st.write(f"**{len(df)} item(s) found**")

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )


# --------------------------------------------------
# MATCHING
# --------------------------------------------------
elif page == "✨ Possible Matches":

    st.title("✨ Possible Item Matches")

    st.write(
        "The system compares lost and found reports using "
        "category, location and item-name similarity."
    )

    matches = find_matches()

    if matches:

        for match in matches:

            with st.container(border=True):

                col1, col2, col3 = st.columns(
                    [2, 2, 1]
                )

                col1.write(
                    f"**Lost:** {match['Lost Item']}"
                )

                col2.write(
                    f"**Found:** {match['Found Item']}"
                )

                col3.metric(
                    "Match",
                    match["Match Score"]
                )

                st.caption(
                    f"Location: {match['Location']}"
                )

    else:

        st.info(
            "No strong matches are currently available."
        )


# --------------------------------------------------
# CLAIMS
# --------------------------------------------------
elif page == "📋 Claims":

    st.title("📋 Item Claims")

    tab1, tab2 = st.tabs(
        ["Submit Claim", "Track Claims"]
    )

    with tab1:

        found_items = [
            item for item in st.session_state["items"]
            if item["Type"] == "Found"
            and item["Status"] == "Available"
        ]

        if found_items:

            item_names = [
                f"{item['ID']} - {item['Name']}"
                for item in found_items
            ]

            selected = st.selectbox(
                "Select Found Item",
                item_names
            )

            claimant = st.text_input(
                "Your Name"
            )

            proof = st.text_area(
                "Proof of Ownership",
                placeholder=(
                    "Describe identifying details that "
                    "prove the item belongs to you..."
                )
            )

            if st.button(
                "Submit Claim",
                type="primary"
            ):

                if claimant and proof:

                    item_name = selected.split(
                        " - ",
                        1
                    )[1]

                    claim_id = (
                        max(
                            [
                                x["Claim ID"]
                                for x in st.session_state.claims
                            ],
                            default=100
                        )
                        + 1
                    )

                    st.session_state.claims.append(
                        {
                            "Claim ID": claim_id,
                            "Item": item_name,
                            "Claimant": claimant,
                            "Proof": proof,
                            "Status": "Pending"
                        }
                    )

                    st.success(
                        f"Claim #{claim_id} submitted!"
                    )

                else:

                    st.warning(
                        "Please provide your name and proof of ownership."
                    )

        else:

            st.info(
                "No found items are currently available for claiming."
            )

    with tab2:

        st.dataframe(
            pd.DataFrame(
                st.session_state.claims
            ),
            use_container_width=True,
            hide_index=True
        )


# --------------------------------------------------
# NOTIFICATIONS
# --------------------------------------------------
elif page == "🔔 Notifications":

    st.title("🔔 Notifications")

    for notification in st.session_state.notifications:

        st.info(
            "🔔 " + notification
        )


# --------------------------------------------------
# ADMIN PANEL
# --------------------------------------------------
elif page == "🛡️ Admin Panel":

    st.title("🛡️ Administrator Panel")

    st.write(
        "Verify ownership claims and manage recovery requests."
    )

    pending = [
        claim for claim in st.session_state.claims
        if claim["Status"] == "Pending"
    ]

    if not pending:

        st.success(
            "There are no pending claims."
        )

    for claim in pending:

        with st.container(border=True):

            st.subheader(
                f"Claim #{claim['Claim ID']}"
            )

            st.write(
                f"**Item:** {claim['Item']}"
            )

            st.write(
                f"**Claimant:** {claim['Claimant']}"
            )

            st.write(
                f"**Ownership Proof:** {claim['Proof']}"
            )

            col1, col2 = st.columns(2)

            if col1.button(
                "✅ Approve",
                key=f"approve_{claim['Claim ID']}"
            ):

                claim["Status"] = "Approved"

                for item in st.session_state["items"]:
                    if item["Name"] == claim["Item"]:
                        item["Status"] = "Recovered"

                st.session_state.notifications.insert(
                    0,
                    f"Claim #{claim['Claim ID']} has been approved."
                )

                st.success(
                    "Claim approved successfully."
                )

                st.rerun()

            if col2.button(
                "❌ Reject",
                key=f"reject_{claim['Claim ID']}"
            ):

                claim["Status"] = "Rejected"

                st.session_state.notifications.insert(
                    0,
                    f"Claim #{claim['Claim ID']} has been rejected."
                )

                st.warning(
                    "Claim rejected."
                )

                st.rerun()

    st.divider()

    st.subheader("All Claims")

    st.dataframe(
        pd.DataFrame(
            st.session_state.claims
        ),
        use_container_width=True,
        hide_index=True
    )


# --------------------------------------------------
# ABOUT
# --------------------------------------------------
elif page == "ℹ️ About Project":

    st.title("ℹ️ About the Project")

    st.subheader(
        "Smart Lost & Found Campus System"
    )

    st.write(
        """
        The Smart Lost & Found Campus System is designed
        to provide a centralized platform for reporting
        and recovering lost belongings within a university
        campus.

        Students can report lost and found items, search
        existing reports, receive possible match suggestions,
        submit ownership claims and track their status.

        Administrators can verify claims and approve or reject
        recovery requests.
        """
    )

    st.subheader("Object-Oriented Design")

    st.write(
        """
        The project uses object-oriented analysis and design
        concepts including:

        - Classes and Objects
        - Encapsulation
        - Inheritance
        - Polymorphism
        - Abstraction
        - Association between system entities
        """
    )

    st.subheader("Major System Classes")

    st.code(
        """
User
 ├── Admin
 └── Student

User ---- reports ----> Item
Item ---- has --------> Claim
Admin --- verifies ---> Claim
System -- sends ------> Notification
        """
    )

    st.subheader("Technology")

    st.write(
        "**Java | OOAD | Python | Streamlit | GitHub**"
    )