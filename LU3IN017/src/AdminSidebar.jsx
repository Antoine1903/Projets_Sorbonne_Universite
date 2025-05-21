import AdminMenu from "./AdminMenu.jsx";
import UserValidation from "./UserValidation.jsx";

function AdminSidebar(props) {
    return (
        <aside>
            <AdminMenu
                currentPage={props.currentPage}
                toFeedPage={props.toFeedPage}
                toFeedAdminPage={props.toFeedAdminPage}
            />
            <UserValidation />
        </aside>
    );
}

export default AdminSidebar;
