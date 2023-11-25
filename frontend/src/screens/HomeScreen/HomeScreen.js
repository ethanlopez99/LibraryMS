import React, { useEffect, useState } from "react";
import MenuItem from "../../components/MenuItem/MenuItem";
import axios from "axios";

import Logo from "../../assets/images/Logo.png";
import "./HomeScreen.css";

import { PiBooksFill, PiArrowCircleUpBold } from "react-icons/pi";
import { FaUserFriends, FaUserShield, FaChartBar } from "react-icons/fa";
import LoanBookModal from "../../components/Modals/LoanBookModal/LoanBookModal";
import ReturnBookModal from "../../components/Modals/ReturnBookModal/ReturnBookModal";
import BooksModal from "../../components/Modals/BooksModal/BooksModal";
import CreateBookModal from "../../components/Modals/CreateBookModal/CreateBookModal";
import CreateLenderModal from "../../components/Modals/CreateLenderModal/CreateLenderModal";

const HomeScreen = ({ userToken, setUserToken }) => {
  // Creating states for modal pages
  const [loanBookModalShow, setLoanBookModalShow] = useState(false);
  const [returnBookModalShow, setReturnBookModalShow] = useState(false);
  const [booksModalShow, setBooksModalShow] = useState(false);
  const [createBookModalShow, setCreateBookModalShow] = useState(false);
  const [createLenderModalShow, setCreateLenderModalShow] = useState(false);

  const [numberOfBooks, setNumberOfBooks] = useState();
  const [numberOfLoans, setNumberOfLoans] = useState();
  const [numberOfLenders, setNumberOfLenders] = useState();
  const [numberOfAdmins, setNumberOfAdmins] = useState();

  useEffect(() => {
    getNumberOfBooks();
    getNumberOfLoans();
    getNumberOfLenders();
    getNumberOfAdmins();
  }, []);
  const getNumberOfBooks = async () => {
    const response = await axios.get("http://127.0.0.1:8000/books/count/all");
    setNumberOfBooks(response.data);
  };
  const getNumberOfLoans = async () => {
    const response = await axios.get(
      "http://127.0.0.1:8000/books/count/unavailable"
    );
    setNumberOfLoans(response.data);
  };
  const getNumberOfLenders = async () => {
    const response = await axios.get("http://127.0.0.1:8000/lenders/count/all");
    setNumberOfLenders(response.data);
  };
  const getNumberOfAdmins = async () => {
    const response = await axios.get("http://127.0.0.1:8000/lenders/count/all");
    setNumberOfAdmins(response.data);
  };

  const menuItems = [
    {
      Icon: PiBooksFill,
      title: "Books",
      value: numberOfBooks,
      color: "green",
      Modal: setBooksModalShow,
    },
    {
      Icon: PiArrowCircleUpBold,
      title: "Current Loans",
      value: numberOfLoans,
      color: "blue",
    },
    {
      Icon: FaUserFriends,
      title: "Lenders",
      value: numberOfLenders,
      color: "orange",
    },
    {
      Icon: FaUserShield,
      title: "Admins",
      value: numberOfAdmins,
      color: "red",
    },
    {
      Icon: FaChartBar,
      title: "Most Popular Books",
      value: 5, // Always shows the top 5 most popular books
      color: "chocolate",
    },
  ];

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
          <div className="dropdown">
            <button className="navbar_button admin_settings">
              Admin Settings
            </button>
            <div className="dropdown_content">
              <a onClick={() => setCreateBookModalShow(true)}>
                Register New Book
              </a>
              <a onClick={() => setCreateLenderModalShow(true)}>
                Register New Lender
              </a>
              <a onClick={() => console.log("test")}>Update Password</a>
            </div>
          </div>
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
            openModal={() => item.Modal(true)}
            key={`${item.title}_item`}
          />
        ))}
      </div>
      {loanBookModalShow && (
        <LoanBookModal
          userToken={userToken}
          setLoanBookModalShow={setLoanBookModalShow}
          getNumberOfLoans={getNumberOfLoans}
        />
      )}
      {returnBookModalShow && (
        <ReturnBookModal
          userToken={userToken}
          setReturnBookModalShow={setReturnBookModalShow}
        />
      )}
      {booksModalShow && (
        <BooksModal
          userToken={userToken}
          setBooksModalShow={setBooksModalShow}
        />
      )}
      {createBookModalShow && (
        <CreateBookModal
          userToken={userToken}
          setCreateBookModalShow={setCreateBookModalShow}
          getNumberOfBooks={getNumberOfBooks}
        />
      )}
      {createLenderModalShow && (
        <CreateLenderModal
          userToken={userToken}
          setCreateLenderModalShow={setCreateLenderModalShow}
          getNumberOfLenders={getNumberOfLenders}
        />
      )}
    </div>
  );
};

export default HomeScreen;
