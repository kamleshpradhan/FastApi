import pytest
from app.calculations import add,subtract,multiply,divide
from app.calculations import BankAccount,InsufficientFunds


@pytest.fixture
def zero_bank_account():
    return BankAccount()

@pytest.fixture
def reg_bank_acccount():
    return BankAccount(50)


@pytest.mark.parametrize("num1, num2, expected",[
    (3, 2, 5),
    (7, 1, 8),
    (12, 4, 16)
])

def test_add(num1,num2,expected):
    assert add(num1,num2) == expected


def test_subtract():
    assert subtract(9,4) == 5


def test_multiple():
    assert multiply(5,4) == 20


def test_divide():
    assert divide(6,3) == 2

# test_add()
# test_divide()
# test_multiple()
# test_subtract()



def test_bank_set_initial_amount(reg_bank_acccount):
    # bank_account = BankAccount(50)
    assert reg_bank_acccount.balance == 50

def test_bank_default_amount(zero_bank_account):
    # bank_account = BankAccount()
    assert zero_bank_account.balance == 0

def test_withdraw(reg_bank_acccount):
    reg_bank_acccount.withdraw(10)
    assert reg_bank_acccount.balance == 40

def test_deposit(reg_bank_acccount):
    reg_bank_acccount.deposit(10)
    assert reg_bank_acccount.balance == 60


def test_collect_intrest(reg_bank_acccount):
    reg_bank_acccount.collect_interest()
    assert round(reg_bank_acccount.balance,6) == 55




@pytest.mark.parametrize('deposited,withdrew,expected',[(200,100,150),(50,10,90)])

def test_bank_transaction(reg_bank_acccount,deposited,withdrew,expected):
    reg_bank_acccount.deposit(deposited)
    reg_bank_acccount.withdraw(withdrew)
    assert reg_bank_acccount.balance == expected

def test_insufficeint_funds(reg_bank_acccount):
    with pytest.raises(InsufficientFunds):
        # which will help pytest to check over exception
        reg_bank_acccount.withdraw(200)

