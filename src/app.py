from solders.pubkey import Pubkey

from .app_context import AppContext

friend_pubkey = Pubkey.from_string("4AN2ePiudKWheFBL7e7GFa1w7HhkUPRv4qfF5WAkvH1C")


def main():
    app = AppContext()
    app.create_collection_nft()
    app.mint_nft()
    app.update_nft()

    # app.transfer_nft(friend_pubkey)

    app.delete_nft()
    # app.update_nft()


main()
