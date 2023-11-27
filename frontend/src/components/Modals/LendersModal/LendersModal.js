import React, { useEffect, useState } from "react";
import axios from "axios";

import "./LendersModal.css";
import Entry from "../../Entry/Entry";

import { IoCloseOutline } from "react-icons/io5";

const LendersModal = ({ setLendersModalShow, userToken }) => {
  const [lenders, setLenders] = useState();
  const [message, setMessage] = useState();


  useEffect(() => {
    getLenders({ target: { value: "" } });
  }, []);

  const getLenders = async (event) => {
    console.log(event.target.value);
    // add request to get books by book name using input
    try {
      const response = await axios.get(
        `http://127.0.0.1:8000/lenders/search?lender_name=%${event.target.value}%`,
        { headers: { Authorization: `Bearer ${userToken}` } }
      );

      const lenders = response.data;
      setLenders(lenders);
    } catch (error) {
      return [];
    }
  };

  const handleUpdate = async (lender) => {
    try {
      const response = await axios.post(
        `http://127.0.0.1:8000/lenders/update`,
        lender,
        { headers: { Authorization: `Bearer ${userToken}` } }
      );
      console.log(response);
      if (response.status === 200) {
        getLenders({ target: { value: "" } });
      }
    } catch (error) {
      console.log(error);
    }
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
          {lenders &&
            lenders.map((lender) => (
              <>
                <Entry lender={lender} handleUpdate={handleUpdate} setErrorMessage={setMessage}/>
                <div style={{ height: "2px", background: "lightgrey" }} />
              </>
            ))}
        </div>
        {message && <h3 style={{color: message.color}}>{message.message}</h3>}

      </div>
    </div>
  );
};

export default LendersModal;
