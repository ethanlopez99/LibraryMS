import React, { useEffect, useState } from "react";
import MenuItem from "../../components/MenuItem/MenuItem";
import axios from "axios";

import Logo from "../../assets/images/Logo.png";
import "./HomeScreen.css";

import { PiBooksFill, PiArrowCircleUpBold } from "react-icons/pi";
import { FaUserFriends, FaUserShield, FaChartBar } from "react-icons/fa";

// Import all modals
import LoanBookModal from "../../components/Modals/LoanBookModal/LoanBookModal";
import ReturnBookModal from "../../components/Modals/ReturnBookModal/ReturnBookModal";
import BooksModal from "../../components/Modals/BooksModal/BooksModal";
import LendersModal from "../../components/Modals/LendersModal/LendersModal";
import TransactionsModal from "../../components/Modals/TransactionsModal/TransactionsModal";
import PopularBooksModal from "../../components/Modals/PopularBooksModal/PopularBooksModal";
import CreateBookModal from "../../components/Modals/CreateBookModal/CreateBookModal";
import CreateLenderModal from "../../components/Modals/CreateLenderModal/CreateLenderModal";
import UpdatePasswordModal from "../../components/Modals/UpdatePasswordModal/UpdatePasswordModal";

const HomeScreen = ({ userToken, setUserToken }) => {
  // Creating states for all modal pages, used to know when to show each
  const [loanBookModalShow, setLoanBookModalShow] = useState(false);
  const [returnBookModalShow, setReturnBookModalShow] = useState(false);
  const [booksModalShow, setBooksModalShow] = useState(false);
  const [lendersModalShow, setLendersModalShow] = useState(false);
  const [transactionsModalShow, setTransactionsModalShow] = useState(false);
  const [popularBooksModalShow, setPopularBooksModalShow] = useState(false);
  const [createBookModalShow, setCreateBookModalShow] = useState(false);
  const [createLenderModalShow, setCreateLenderModalShow] = useState(false);
  const [updatePasswordModalShow, setUpdatePasswordModalShow] = useState(false);

  // Variables created to show number of entries for each of the dashboard items
  const [numberOfBooks, setNumberOfBooks] = useState();
  const [numberOfLoans, setNumberOfLoans] = useState();
  const [numberOfLenders, setNumberOfLenders] = useState();
  const [numberOfAdmins, setNumberOfAdmins] = useState();

  // Get all initial values at the beginning, only once (thus "[]")
  useEffect(() => {
    getNumberOfBooks();
    getNumberOfLoans();
    getNumberOfLenders();
    getNumberOfAdmins();
  }, []);
  // Get number of books in database
  const getNumberOfBooks = async () => {
    const response = await axios.get("http://127.0.0.1:8000/books/count/all");
    setNumberOfBooks(response.data);
  };
  // Get number of loans in database (i.e., unavailable books)
  const getNumberOfLoans = async () => {
    const response = await axios.get(
      "http://127.0.0.1:8000/books/count/unavailable"
    );
    setNumberOfLoans(response.data);
  };

  // Get number of lenders from the database
  const getNumberOfLenders = async () => {
    const response = await axios.get("http://127.0.0.1:8000/lenders/count/all");
    setNumberOfLenders(response.data);
  };

  // Get number of admins from the database
  const getNumberOfAdmins = async () => {
    const response = await axios.get("http://127.0.0.1:8000/lenders/count/all");
    setNumberOfAdmins(response.data);
  };

  // Define each of the dashboard items, with the modals they open up
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
      Modal: setTransactionsModalShow,
    },
    {
      Icon: FaUserFriends,
      title: "Lenders",
      value: numberOfLenders,
      color: "orange",
      Modal: setLendersModalShow,
    },
    {
      Icon: FaUserShield,
      title: "Admins",
      value: numberOfAdmins,
      color: "red",
      Modal: (input) => console.log(input),
    },
    {
      Icon: FaChartBar,
      title: "Most Popular Books",
      value: 5, // Always shows the top 5 most popular books
      color: "chocolate",
      Modal: setPopularBooksModalShow,
    },
  ];

  // Remove user token to log out and bring user back to login
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
              <a onClick={() => setUpdatePasswordModalShow(true)}>
                Update Password
              </a>
            </div>
          </div>
        </div>
        <div style={{ height: "5px", background: "purple" }} />
      </nav>
      <div className="app_home-dashboard_container">
        {/* Add each of the items to the dashboard as a MenuItem object */}
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
      {/* Show each of the modals, based on their values set to true */}
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
          getNumberOfLoans={getNumberOfLoans}
        />
      )}
      {booksModalShow && (
        <BooksModal
          userToken={userToken}
          setBooksModalShow={setBooksModalShow}
          count={numberOfBooks}
        />
      )}
      {lendersModalShow && (
        <LendersModal
          userToken={userToken}
          setLendersModalShow={setLendersModalShow}
          count={numberOfLenders}
        />
      )}
      {transactionsModalShow && (
        <TransactionsModal
          userToken={userToken}
          setTransactionsModalShow={setTransactionsModalShow}
          numberOfLoans={numberOfLoans}
        />
      )}
      {popularBooksModalShow && (
        <PopularBooksModal
          userToken={userToken}
          setPopularBooksModalShow={setPopularBooksModalShow}
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
      {updatePasswordModalShow && (
        <UpdatePasswordModal
          userToken={userToken}
          setUpdatePasswordModalShow={setUpdatePasswordModalShow}
          setUserToken={setUserToken}
        />
      )}
    </div>
  );
};

export default HomeScreen;
