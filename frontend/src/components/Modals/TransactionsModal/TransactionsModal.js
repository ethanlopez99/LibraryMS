
import BooksModal from "../BooksModal/BooksModal";


function TransactionsModal({userToken, setTransactionsModalShow, getNumberOfLoans}){


    return (
        <>
            <BooksModal unavailable={true} setTransactionsModalShow={setTransactionsModalShow} userToken={userToken} />
        </>
  );
};

export default TransactionsModal;
