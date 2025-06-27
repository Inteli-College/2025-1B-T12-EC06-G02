export default function Loading () {
    return(
        <div className="min-h-screen flex items-center justify-center">
        <svg
          className="animate-spin h-10 w-10 md:h-44 md:w-44 text-[#00C939]"
          xmlns="http://www.w3.org/2000/svg"
          fill="none"
          viewBox="0 0 24 24"
        >
          <circle
            className="opacity-55"
            cx="12"
            cy="12"
            r="10"
            stroke="currentColor"
            strokeWidth="4"
          ></circle>
          <path
            className="opacity-75"
            fill="currentColor"
            d="M4 12a8 8 0 018-8v8H4z"
          ></path>
        </svg>
      </div>
    )
}