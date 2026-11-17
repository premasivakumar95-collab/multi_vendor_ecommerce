function AdminDashboard() {
  return (
    <div className="dashboard">
      <h1>Admin Dashboard</h1>
      <h3>Welcome, Admin!</h3>

      <div className="dashboard-grid">
        <div className="box">Total Users</div>
        <div className="box">Total Vendors</div>
        <div className="box">Total Customers</div>
      </div>

      <h2>User Management</h2>
      <p>Manage registered users and account status.</p>
    </div>
  );
}

export default AdminDashboard;
