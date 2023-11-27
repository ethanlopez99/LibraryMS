
import BooksModal from "../BooksModal/BooksModal";


function TransactionsModal({userToken, setTransactionsModalShow}){


    return (
        <>
            <BooksModal unavailable={true} setTransactionsModalShow={setTransactionsModalShow}/>
        </>
  );
};

export default TransactionsModal;
