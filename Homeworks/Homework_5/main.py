from transfers_script import add_bank, add_user, add_account, modify_bank, modify_user, modify_account, transfer_money


def main():
    add_bank(('Bank1',), ('Bank2',))
    add_bank([('Bank5',), ('Bank6',)])

    add_user(('Petro Poroshenko', '12-03-2005', 'ID--j4%43213547-u9'),
             ('Maryna Paroshenko', '13-03-2005', 'ID--j4%43263147-u9'))
    add_user([('Petro Petrovych', '12-03-2005', 'ID--j4-23213547-u9'),
              ('Maryna Marynivna', '13-03-2005', 'ID--j4-13263147-u9')])

    add_account((2, 'credit', 422, 2, 'USD', 15.0, 'gold'),
                (4, 'credit', 228, 3, 'EUR', 20.0, 'silver'))
    add_account([(2, 'debit', 123, 2, 'CAD', 300.0, 'gold'),
                (4, 'debit', 456, 3, 'USD', 1.0, 'platinum')])

    modify_bank('Bank_Test', 2)
    modify_user('Volodymyr', 'Big', '01-01-1988', 'ID--j4%43213547-f5', 2)
    modify_account(2, 'credit', 152, 4, 'EUR', 15.0, 'gold', 2)

    transfer_money(2, 3, 9.99)


if __name__ == '__main__':
    main()
