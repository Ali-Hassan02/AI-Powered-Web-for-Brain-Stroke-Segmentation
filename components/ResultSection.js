import { CircularProgress } from "@mui/material";

const ResultSection = ({
  imageSlices,
  segmentationSlices,
  currentSlice,
  handleNextSlice,
  handlePrevSlice,
  loading, // New prop to control the loader
}) => {
  return (
    <div className="mt-0 sm:mt-0 flex flex-col sm:flex-row gap-8 justify-center w-full">
      {loading ? (
        // Show the Material-UI loader
        <div className="flex justify-center items-center w-full h-[400px]">
          <CircularProgress color="primary" size={50} />
        </div>
      ) : (
        imageSlices.length > 0 && (
          <div className="p-6 sm:p-8 lg:p-12 rounded-lg text-center w-full sm:w-11/12 md:w-5/6 lg:w-4/5 xl:w-3/4 h-auto max-h-[400px]">
            <div className="flex flex-col lg:flex-row gap-8 justify-center items-center">
              {/* Brain Slice Section */}
              <div className="flex flex-col items-center w-full lg:w-1/2">
                <h2 className="text-xl sm:text-2xl text-blue-500 mb-4">
                  Brain Slice - {currentSlice + 1} / {imageSlices.length}
                </h2>
                <img
                  src={`data:image/png;base64,${imageSlices[currentSlice]}`}
                  alt={`MRI Slice ${currentSlice}`}
                  className="w-full max-w-sm sm:max-w-md lg:max-w-md xl:max-w-lg rounded-lg mb-4"
                />
              </div>

              {/* Stroke Prediction Section */}
              <div className="flex flex-col items-center w-full lg:w-1/2">
                <h2 className="text-xl sm:text-2xl text-blue-500 mb-4">
                  Stroke Prediction
                </h2>
                <img
                  src={`data:image/png;base64,${segmentationSlices[currentSlice]}`}
                  alt={`Segmentation Slice ${currentSlice}`}
                  className="w-full max-w-sm sm:max-w-md lg:max-w-md xl:max-w-lg rounded-lg mb-4"
                />
              </div>
            </div>

            {/* Navigation Buttons */}
            <div className="flex justify-center gap-4 mt-6">
              <button
                onClick={handlePrevSlice}
                disabled={currentSlice === 0}
                className="px-4 py-2 bg-gray-300 text-gray-800 rounded-lg disabled:opacity-50"
              >
                Previous
              </button>
              <button
                onClick={handleNextSlice}
                disabled={currentSlice === imageSlices.length - 1}
                className="px-4 py-2 bg-gray-300 text-gray-800 rounded-lg disabled:opacity-50"
              >
                Next
              </button>
            </div>
          </div>
        )
      )}
    </div>
  );
};

export default ResultSection;
