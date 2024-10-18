FROM rasa/rasa:3.6.0-full

# Copy your Rasa model and any other necessary files
COPY ./ /app
WORKDIR /app

# Expose the default Rasa port
EXPOSE 5005

# Command to run the Rasa server
CMD ["rasa", "run", "--enable-api", "--cors", "*", "--debug"]
