from ext import app



if __name__ == "__main__":
    from routes import home,music_mastering,music_mixing,music_production,music_theory,login,register,post,forum, remove_post, profile, edit, delete_all, all_users, delete_user, make_post
    app.run(debug=True)
