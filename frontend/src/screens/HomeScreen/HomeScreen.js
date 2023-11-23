import React from "react";
import axios from "axios";
import MenuItem from "../../components/MenuItem/MenuItem";

import Logo from "../../assets/images/Logo.png";
import "./HomeScreen.css";

import { PiBooksFill, PiArrowCircleUpBold } from "react-icons/pi";
import { FaUserFriends, FaUserShield, FaChartBar } from "react-icons/fa";

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
  const handleLogout = () => {
    setUserToken(null);
  };
  const handleModal = () => {
    console.log("test");
  };

  return (
    <div className="app_home">
      <header className="app_home-header">
        <img src={Logo} />
        <button type="button" onClick={handleLogout}>
          Log Out
        </button>
      </header>
      <nav className="app_home-navbar"></nav>
      <div className="app_home-dashboard_container">
        {menuItems.map((item) => (
          <MenuItem
            Icon={item.Icon}
            title={item.title}
            value={item.value}
            color={item.color}
            openModal={handleModal}
            key={`${item.title}_item`}
          />
        ))}
      </div>
    </div>
  );
};

export default HomeScreen;
