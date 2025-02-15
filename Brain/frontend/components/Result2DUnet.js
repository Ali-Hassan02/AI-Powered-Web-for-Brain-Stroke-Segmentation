import React from "react";

const Result2DUnet = ({ image, segmentation, loading }) => {
  return (
    <div className="w-full flex flex-col items-center">
      {loading ? (
        <div className="flex justify-center items-center">
          <span className="text-xl text-gray-700">Loading...</span>
        </div>
      ) : (
        <>
          <div className="mb-6">
            <h2 className="text-2xl text-gray-800">Original Image</h2>
            <img
              src={image}
              alt="Original Brain Scan"
              className="w-96 h-auto mt-4 border shadow-md"
            />
          </div>
          <div className="mb-6">
            <h2 className="text-2xl text-gray-800">Predicted Stroke Mask</h2>
            <img
              src={segmentation}
              alt="Predicted Stroke"
              className="w-96 h-auto mt-4 border shadow-md"
            />
          </div>
        </>
      )}
    </div>
  );
};

export default Result2DUnet;
