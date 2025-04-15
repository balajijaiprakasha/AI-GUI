import React from "react";

export const Button = ({ children, onClick }) => {
  return (
    <button
      className="bg-black text-white px-4 py-2 rounded mt-2"
      onClick={onClick}
    >
      {children}
    </button>
  );
};
