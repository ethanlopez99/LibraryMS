import React, { useEffect, useState } from "react";
import axios from "axios";

import "./LendersModal.css";
import Entry from "../../Entry/Entry";

import Pagination from "@mui/material/Pagination";
import { IoCloseOutline } from "react-icons/io5";

// Lenders modal defined
const LendersModal = ({ setLendersModalShow, userToken, count }) => {
  const [lenders, setLenders] = useState();
  const [page, setPage] = useState(1);
  const [message, setMessage] = useState();

  // on load, get all lenders (backend will limit to 10)
  useEffect(() => {
    getLenders({ target: { value: "" }, skip: page * 10 - 10 });
  }, []);

  // get all lenders from API. Using "event" as input here to match input component's syntax
  const getLenders = async ({ target, skip }) => {
    try {
      // make get request to api for lenders matching name
      const response = await axios.get(
        `http://127.0.0.1:8000/lenders/search?lender_name=%${target.value}%&skip=${skip}`,
        { headers: { Authorization: `Bearer ${userToken}` } }
      );

      // retrieve response and assign to lenders
      const lenders = response.data;
      // set lenders as response data
      setLenders(lenders);
    } catch (error) {
      // log error to console for further debugging by user if needed
      console.log(error);
      // If error retrieving lenders, let user know
      setMessage({
        message: "Error retrieving lenders, please try again",
        color: "red",
      });
    }
  };

  // handle lender update given a lender object (input will contain new values, with original id)
  const handleUpdate = async (lender) => {
    try {
      const response = await axios.post(
        `http://127.0.0.1:8000/lenders/update`,
        lender,
        { headers: { Authorization: `Bearer ${userToken}` } }
      );
      if (response.status === 200) {
        // if post request response is ok, lenders list is updated
        getLenders({ target: { value: "" }, skip: page * 10 - 10 });
      }
    } catch (error) {
      // log error to console for further debugging by user if needed
      console.log(error);
      // If error updating lender, let user know
      setMessage({
        message: error.response.data.detail,
        color: "red",
      });
    }
  };

  const handlePageChange = (event, value) => {
    setPage(value);
    getLenders({ target: { value: "" }, skip: value * 10 - 10 });
    setMessage();
  };

  return (
    <div className="modal_bg">
      <div className="app_modal books_modal">
        <div className="app_modal-close">
          <IoCloseOutline
            size={50}
            onClick={() => setLendersModalShow(false)}
            color="grey"
          />
        </div>
        <h1>All Lenders</h1>
        <div className="selection_container_books_modal">
          <h3>Lender Name</h3>
          <input onChange={getLenders} />
        </div>

        <div style={{ width: "80%", flex: "3" }}>
          {/* map every lender to a new Entry component */}
          {lenders &&
            lenders.map((lender) => (
              <>
                <Entry
                  lender={lender}
                  handleUpdate={handleUpdate}
                  setErrorMessage={setMessage}
                />
                <div style={{ height: "2px", background: "lightgrey" }} />
              </>
            ))}
        </div>
        <Pagination count={Math.ceil(count / 10)} onChange={handlePageChange} />
        {/* show error message if any */}
        {message && <h3 style={{ color: message.color }}>{message.message}</h3>}
      </div>
    </div>
  );
};

export default LendersModal;
