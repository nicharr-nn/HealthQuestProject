// async function logout() {
//   try {
//     await fetch("http://localhost:8000/api/logout/", {
//       method: "POST",
//       credentials: "include", // important to send cookies!
//     });
//     // Clear any local state (if you store user info)
//     localStorage.removeItem("user");
//     window.location.href = "/"; // redirect to homepage/login page
//   } catch (err) {
//     console.error("Logout failed", err);
//   }
// }
