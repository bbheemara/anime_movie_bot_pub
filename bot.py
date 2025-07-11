from telegram import Update,InlineKeyboardButton , InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes,CallbackQueryHandler

from typing import Final
import requests
import random





TOKEN : Final='NONE'
BOT_USERNAME: Final= '@anime_movie_kb_bot'


async def start_command(update: Update , context:ContextTypes.DEFAULT_TYPE):
    keyboard=[
         
         [InlineKeyboardButton('✨ Anime',callback_data='anime')],
         [InlineKeyboardButton('🍿 Movie', callback_data='movie')]
    ]
    reply_markup=InlineKeyboardMarkup(keyboard)  
    
    await update.message.reply_text('Hello there!👋 What would you like to expolore today? 😈', reply_markup=reply_markup)
    
async def help_command(update:Update, context:ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('THis is help commnd the the following are commands:' \
    'help')

async def custom_command(update: Update, context:ContextTypes.DEFAULT_TYPE): 
     await update.message.reply_text('This is custom command responce')


async def handle_choice(update:Update, context: ContextTypes.DEFAULT_TYPE):
     
     query=update.callback_query
     await query.answer()
     

     choice=query.data

     if choice == 'anime':
        genre_buttons=[
             [InlineKeyboardButton("Action 🔥",callback_data='genre_action')],
             [InlineKeyboardButton("Comedy 😂",callback_data='genre_comedy')],
             [InlineKeyboardButton("Romance ❤️", callback_data='genre_romance')],
             [InlineKeyboardButton("Drama 🎭" , callback_data='genre_drama')],
             [InlineKeyboardButton("Sci-Fi 🌌",callback_data='genre_scifi')],
             [InlineKeyboardButton("Fantasy 🧚",callback_data='genre_fantasy')]



        ]
        reply_markup=InlineKeyboardMarkup(genre_buttons)
        await query.edit_message_text("🔥Select a genre to get a recommendation:", reply_markup=reply_markup)

     elif choice == 'movie':
          genre_buttons = [
        [InlineKeyboardButton("Action 🎬", callback_data='movie_action')],
        [InlineKeyboardButton("Comedy 😂", callback_data='movie_comedy')],
        [InlineKeyboardButton("Drama 🎭", callback_data='movie_drama')],
        [InlineKeyboardButton("Romance ❤️", callback_data='movie_romance')],
        [InlineKeyboardButton("Horror 👻", callback_data='movie_horror')],
        [InlineKeyboardButton("Sci-Fi 🚀", callback_data='movie_scifi')],
               ]
          reply_markup= InlineKeyboardMarkup(genre_buttons)
          await query.edit_message_text("🎞 Select a movie genre to get a suggestion:", reply_markup=reply_markup)




GENRE_MAP ={
     'genre_action':1,
     'genre_comedy':4,
     'genre_romance':22,
     'genre_drama':8,
     'genre_scifi': 24,
     'genre_fantasy':10   
}



async def handle_genre_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    genre_key = query.data
    genre_id = GENRE_MAP.get(genre_key)

    if not genre_id:
        await query.edit_message_text("Unknown genre.")
        return

    url = f"https://api.jikan.moe/v4/anime?genres={genre_id}&order_by=score&sort=desc&limit=25"
    
    try:
        response = requests.get(url).json()

        if 'data' not in response or not response['data']:
            await query.edit_message_text("No anime found in that genre.")
            return

        anime = random.choice(response['data'])
        title = anime['title']
        score = anime.get('score', 'N/A')
        synopsis = anime.get('synopsis', 'No synopsis available')[:300] + '...'
        url_link = anime['url']
        img_url = anime['images']['jpg']['image_url']
        anime_type = anime.get('type', 'Unknown')
        episodes = anime.get('episodes', 'N/A')
        mal_id = anime['mal_id']

        message = (
            f"🎬 *{title}*\n"
            f"🎞 Type: {anime_type} | 🧩 Episodes: {episodes}\n"
            f"⭐ Score: {score}\n"
            f"📖 {synopsis}\n"
            f"🌍 [More Info]({url_link})"
        )

        buttons = [
            [InlineKeyboardButton("🔁 Suggest Similar", callback_data=f"similar_anime_{mal_id}")]
        ]
        markup = InlineKeyboardMarkup(buttons)

        await context.bot.send_photo(
            chat_id=query.message.chat.id,
            photo=img_url,
            caption=message,
            parse_mode='Markdown',
            reply_markup=markup
        )

    except Exception as e:
        print("❌ ERROR while parsing/sending anime:")
        print(e)
        await query.edit_message_text("Something went wrong while fetching anime 😓")



async def handle_similar_anime(update: Update, context: ContextTypes.DEFAULT_TYPE):
     query=update.callback_query
     await query.answer()


     anime_id=query.data.split("_")[-1]
     
     url = f"https://api.jikan.moe/v4/anime/{anime_id}/recommendations"

     try:
          response=requests.get(url).json()

          recommendations=response.get('data', []) 

          if not recommendations:
               await query.edit_message_text("No similar anime found.")

               return
          recommended=random.choice(recommendations).get('entry')

          title = recommended['title']
          url_link = recommended['url']
          img_url = recommended['images']['jpg']['image_url']
          mal_id = recommended['mal_id']

          details_url = f"https://api.jikan.moe/v4/anime/{mal_id}"
          details = requests.get(details_url).json().get("data", {})

          score = details.get('score', 'N/A')
          synopsis = details.get('synopsis', 'No synopsis available')[:300] + '...'
          anime_type = details.get('type', 'Unknown')
          episodes = details.get('episodes', 'N/A')

          caption = (
          f"🎬 *{title}*\n"
          f"🎞 Type: {anime_type} | 🧩 Episodes: {episodes}\n"
          f"⭐ Score: {score}\n"
          f"📖 {synopsis}\n"
          f"🌍 [More Info]({url_link})"
          )
          

          buttons=[
         [InlineKeyboardButton("🔁 Suggest Another", callback_data=f"similar_anime_{recommended['mal_id']}")]

         ]
          markup=InlineKeyboardMarkup(buttons)

          await context.bot.send_photo(
    chat_id=query.message.chat.id,
    photo=img_url,
    caption=caption,        
    parse_mode="Markdown",
    reply_markup=markup
)


          


     except Exception as e:
                  print("❌ ERROR while fetching similar anime:", e)
                  await query.edit_message_text("Something went wrong while finding similar anime.")















import random

TMDB_API_KEY = "d845ee0054920ffc2fef771c476322b8"
GENRE_IDS = {
    'movie_action': 28,
    'movie_comedy': 35,
    'movie_drama': 18,
    'movie_romance': 10749,
    'movie_horror': 27,
    'movie_scifi': 878
}

async def handle_movie_genre(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    genre_key = query.data
    genre_id = GENRE_IDS.get(genre_key)

    if not genre_id:
        await query.edit_message_text("Unknown movie genre.")
        return

    url = (
        f"https://api.themoviedb.org/3/discover/movie"
        f"?api_key={TMDB_API_KEY}"
        f"&with_genres={genre_id}"
        f"&sort_by=popularity.desc"
        f"&language=en-US"
        f"&include_adult=false"
        f"&vote_count.gte=50"
    )

    try:
        response = requests.get(url).json()
        movies = response.get("results", [])

        if not movies:
            await query.edit_message_text("No movies found for this genre.")
            return

        movie = random.choice(movies)
        title = movie.get("title", "Unknown Title")
        overview = movie.get("overview", "No description available")[:300] + "..."
        poster_path = movie.get("poster_path", "")
        rating = movie.get("vote_average", "N/A")
        release = movie.get("release_date", "N/A")
        imdb_url = f"https://www.themoviedb.org/movie/{movie['id']}"

        caption = (
            f"🎬 *{title}* ({release})\n"
            f"⭐ Rating: {rating}\n"
            f"📖 {overview}\n"
            f"🔗 [More Info]({imdb_url})"
        )

        buttons = [
       [InlineKeyboardButton("🔁 Suggest Similar", callback_data=f"similar_movie_{movie['id']}")]
                                   ]
        reply_markup = InlineKeyboardMarkup(buttons)

        if poster_path:
            image_url = f"https://image.tmdb.org/t/p/w500{poster_path}"
            await context.bot.send_photo(
                chat_id=query.message.chat.id,
                photo=image_url,
                caption=caption,
                parse_mode="Markdown"
            )
            
        else:
            await context.bot.send_message(
                chat_id=query.message.chat.id,
                text=caption,
                parse_mode="Markdown"
            )

    except Exception as e:
        print("❌ ERROR while fetching movie:", e)
        await query.edit_message_text("Too many requests by you!! i can't handle 😓")



async def handle_similar_movie(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    movie_id = query.data.split("_")[-1]
    url = f"https://api.themoviedb.org/3/movie/{movie_id}/similar?api_key={TMDB_API_KEY}&language=en-US&page=1"

    try:
        response = requests.get(url).json()
        results = response.get("results", [])

        if not results:
            await query.edit_message_text("No similar movies found.")
            return

        movie = random.choice(results)
        title = movie.get("title", "Unknown Title")
        overview = movie.get("overview", "No description available")[:300] + "..."
        poster_path = movie.get("poster_path", "")
        rating = movie.get("vote_average", "N/A")
        release = movie.get("release_date", "N/A")
        imdb_url = f"https://www.themoviedb.org/movie/{movie['id']}"

        caption = (
            f"🎬 *{title}* ({release})\n"
            f"⭐ Rating: {rating}\n"
            f"📖 {overview}\n"
            f"🔗 [More Info]({imdb_url})"
        )

        buttons = [
            [InlineKeyboardButton("🔁 Suggest Another", callback_data=f"similar_movie_{movie['id']}")]
        ]
        reply_markup = InlineKeyboardMarkup(buttons)

        if poster_path:
            image_url = f"https://image.tmdb.org/t/p/w500{poster_path}"
            await context.bot.send_photo(
                chat_id=query.message.chat.id,
                photo=image_url,
                caption=caption,
                parse_mode="Markdown",
                reply_markup=reply_markup
            )
        else:
            await context.bot.send_message(
                chat_id=query.message.chat.id,
                text=caption,
                parse_mode="Markdown",
                reply_markup=reply_markup
            )
    except Exception as e:
        print("❌ ERROR while fetching similar movie:", e)
        await query.edit_message_text("Something went wrong while finding similar movie.")


def handle_response(text:str ) :
     processed: str =text.lower()

     if 'hello' in processed:
          return 'Hey there 😉'
     
     if 'how are you' in processed:
          return 'I am a bot fool 😒 '
     if 'anime' in processed:
          return 'ONEPIECE? ❤️‍🔥'
     
     return 'wtf did u send'
     



async def handle_message( update: Update , context: ContextTypes.DEFAULT_TYPE):
      message_type:str = update.message.chat.type
      text:str = update.message.text

      print(f'User ({update.message.chat.id}) in {message_type}: "{text}"')
   
      if message_type == 'group':
           if BOT_USERNAME in text:
                new_text:str = text.replace(BOT_USERNAME,'').strip()
                responce:str= handle_response(new_text)
           else:
                return      

          
      else:
           responce:str=handle_response(text)

      await update.message.reply_text(responce)



async def error(update:Update,context:ContextTypes.DEFAULT_TYPE):
     print(f'Update {update} caused error {context.error}')



if __name__== '__main__':
          print('Starting bot...')
          app=Application.builder().token(TOKEN).build()
          app.add_handler(CallbackQueryHandler(handle_genre_callback, pattern='^genre_'))
          app.add_handler(CallbackQueryHandler(handle_similar_anime, pattern="^similar_anime_"))

          app.add_handler(CallbackQueryHandler(handle_movie_genre, pattern='^movie_'))
          app.add_handler(CallbackQueryHandler(handle_similar_movie, pattern="^similar_movie_"))


          app.add_handler(CallbackQueryHandler(handle_choice)) 
          app.add_handler(CommandHandler('start', start_command))
          app.add_handler(CommandHandler('help',help_command))
          app.add_handler(CommandHandler('Custom',custom_command))
          


          app.add_handler(MessageHandler(filters.TEXT, handle_message))
        
          app.add_error_handler(error)
          print('polling...')
          app.run_polling(poll_interval=3)









  




           







