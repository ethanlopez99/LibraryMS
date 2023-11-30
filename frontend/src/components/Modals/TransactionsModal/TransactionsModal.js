import BooksModal from "../BooksModal/BooksModal";

function TransactionsModal({
  userToken,
  setTransactionsModalShow,
  numberOfLoans,
}) {
  return (
    <>
      {/* Calls BooksModal, with unavailable prop set to true, to find all unavailable books */}
      <BooksModal
        unavailable={true}
        setTransactionsModalShow={setTransactionsModalShow}
        userToken={userToken}
        count={numberOfLoans}
      />
    </>
  );
}

export default TransactionsModal;
