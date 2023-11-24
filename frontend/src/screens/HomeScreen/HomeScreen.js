import React, { useState } from "react";
import MenuItem from "../../components/MenuItem/MenuItem";

import Logo from "../../assets/images/Logo.png";
import "./HomeScreen.css";

import { PiBooksFill, PiArrowCircleUpBold } from "react-icons/pi";
import { FaUserFriends, FaUserShield, FaChartBar } from "react-icons/fa";
import LoanBookModal from "../../components/Modals/LoanBookModal/LoanBookModal";
import ReturnBookModal from "../../components/Modals/ReturnBookModal/ReturnBookModal";

const menuItems = [
  { Icon: PiBooksFill, title: "Books", value: 10, color: "green" },
  {
    Icon: PiArrowCircleUpBold,
    title: "Current Loans",
    value: 10,
    color: "blue",
  },
  { Icon: FaUserFriends, title: "Lenders", value: 10, color: "orange" },
  { Icon: FaUserShield, title: "Admins", value: 10, color: "red" },
  {
    Icon: FaChartBar,
    title: "Most Popular Books",
    value: 10,
    color: "chocolate",
  },
];

const HomeScreen = ({ userToken, setUserToken }) => {
  // Creating states for modal pages
  const [loanBookModalShow, setLoanBookModalShow] = useState(false);
  const [returnBookModalShow, setReturnBookModalShow] = useState(false);

  const handleLogout = () => {
    setUserToken(null);
  };

  return (
    <div className="app_home">
      <header className="app_home-header">
        <img src={Logo} />
        <button type="button" onClick={handleLogout}>
          Log Out
        </button>
      </header>
      <nav className="app_home-navbar">
        <div className="app_home-navbar_container">
          <button
            className="navbar_button"
            onClick={() => setLoanBookModalShow(true)}
          >
            Loan Book
          </button>
          <button
            className="navbar_button"
            onClick={() => setReturnBookModalShow(true)}
          >
            Return Book
          </button>
        </div>
        <div style={{ height: "5px", background: "purple" }} />
      </nav>
      <div className="app_home-dashboard_container">
        {menuItems.map((item) => (
          <MenuItem
            Icon={item.Icon}
            title={item.title}
            value={item.value}
            color={item.color}
            openModal={() => console.log(item.title)}
            key={`${item.title}_item`}
          />
        ))}
      </div>
      {loanBookModalShow && (
        <LoanBookModal
          userToken={userToken}
          setLoanBookModalShow={setLoanBookModalShow}
        />
      )}
      {returnBookModalShow && (
        <ReturnBookModal
          userToken={userToken}
          setReturnBookModalShow={setReturnBookModalShow}
        />
      )}
    </div>
  );
};

export default HomeScreen;
