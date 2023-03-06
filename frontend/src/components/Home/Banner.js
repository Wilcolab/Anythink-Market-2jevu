import React from "react";
import logo from "../../imgs/logo.png";
import SearchBar from "./SearchBar";

const Banner = ({ setSearch }) => {
  return (
    <div className="banner text-white">
      <div className="container p-4 text-center">
        <img src={logo} alt="banner" />
        <div>
          <span>A place to </span>
          <span id="get-part">get </span>
          <SearchBar setSearchTerm={setSearch} />
          <span> the cool stuff.</span>
        </div>
      </div>
    </div>
  );
};

export default Banner;
