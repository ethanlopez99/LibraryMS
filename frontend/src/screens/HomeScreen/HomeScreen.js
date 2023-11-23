import React from "react";
import axios from "axios";
import MenuItem from "../../components/MenuItem/MenuItem";

import { PiBooksFill } from "react-icons/pi";

const HomeScreen = ({ userToken, setUserToken }) => {
  const handleLogout = () => {
    setUserToken(null);
  };
  return (
    <div>
      <button type="button" onClick={handleLogout}>
        Log Out
      </button>
      <MenuItem Icon={PiBooksFill} title="Books" value={10} color="green" />
    </div>
  );
};

export default HomeScreen;
