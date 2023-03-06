import React, { useState, useEffect } from "react";

const SearchBar = ({ setSearchTerm }) => {
  const [tmpSearchTerm, setTmpSearchTerm] = useState("");

  useEffect(() => {
    if (tmpSearchTerm.length >= 3) {
      setSearchTerm(tmpSearchTerm);
    }
  }, [tmpSearchTerm, setSearchTerm]);

  return (
    <form id="search-box">
      <input
        type="text"
        placeholder="What is it that you truly desire?"
        value={tmpSearchTerm}
        onChange={(e) => setTmpSearchTerm(e.target.value)}
      />
    </form>
  );
};

export default SearchBar;
