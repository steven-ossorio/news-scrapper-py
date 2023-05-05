import openai


class OpenAI:
    """
    A class for interacting with the OpenAI API.

    Args:
        model (str): The name of the OpenAI model to use. Default is "text-davinci-003".
        prompt (str): The prompt to use for generating text. Default is an empty string.
        temperature (float): The sampling temperature to use for generating text. Default is 0.8.
        max_tokens (int): The maximum number of tokens to generate for each request. Default is 120.

    """

    def __init__(self, model: str = "text-davinci-003", prompt: str = "", temperature: float = 0.8, max_tokens: int = 120):
        """
        Initializes an OpenAI object with the given parameters.
        """

        self.model = model
        self.prompt = prompt
        self.temperature = temperature
        self.max_tokens = max_tokens

    def summarize_text(self, text: str) -> str:
        """
        Summarizes the given text using the OpenAI API.

        Args:
            text (str): The text to summarize.

        Returns:
            str: A summary of the given text.

        Raises:
            Exception: If there is an error calling the OpenAI API.
        """

        try:
            response = openai.Completion.create(
                model=self.model,
                prompt=f"Give me a summary of {text}",
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )

            summary = response['choices'][0]['text'].replace('\n', '')

            return summary

        except Exception as e:
            raise Exception("Error calling OpenAI API: " + str(e))

    def translate_text(self, text: str, language: str) -> str:
        """
        Translates the given text to the specified language using the OpenAI API.

        Args:
            text (str): The text to translate.
            language (str): The language to translate to.

        Returns:
            str: The translated text.

        Raises:
            Exception: If there is an error calling the OpenAI API.
        """

        try:
            response = openai.Completion.create(
                model=self.model,
                prompt=f"Translate {text} to {language}",
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )

            translation = response['choices'][0]['text'].replace('\n', '')

            return translation

        except Exception as e:
            raise Exception("Error calling OpenAI API: " + str(e))
