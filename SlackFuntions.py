class SlackFunctions:
    @staticmethod
    def get_has_reaction_messages(messages):
        return_messages = []
        for msg in messages:
            if 'reactions' in msg:
                return_messages.append(msg)
        return return_messages

    @staticmethod
    def get_text_in_messages(messages):
        return_text = []
        for msg in messages:
            return_text.append(msg['text'])
        return return_text
