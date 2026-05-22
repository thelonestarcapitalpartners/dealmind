import React from 'react';
import { View, StyleSheet, ScrollView, FlatList } from 'react-native';
import { Text, TextInput, Button } from 'react-native-paper';

/**
 * Deal Chat Screen - Chat with AI about the deal
 * 
 * Features:
 * - Send messages
 * - Ask scenario questions
 * - Generate documents
 * - See AI responses with calculations
 */
export default function DealChatScreen({ navigation, route }) {
  const { dealId } = route.params;
  const [messages, setMessages] = React.useState([]);
  const [inputText, setInputText] = React.useState('');

  const handleSendMessage = async () => {
    if (!inputText.trim()) return;

    // Add user message
    const userMessage = { id: Date.now(), role: 'user', content: inputText };
    setMessages(prev => [...prev, userMessage]);
    setInputText('');

    // TODO: Call chat API and get AI response
    // const response = await callChatAPI(dealId, inputText);
    // setMessages(prev => [...prev, { id: Date.now(), role: 'assistant', content: response }]);
  };

  return (
    <View style={styles.container}>
      <FlatList
        data={messages}
        keyExtractor={item => item.id.toString()}
        renderItem={({ item }) => (
          <ChatMessage message={item} />
        )}
        style={styles.messagesList}
        contentContainerStyle={styles.messagesContainer}
      />

      <View style={styles.inputArea}>
        <TextInput
          placeholder="Ask me anything about this deal..."
          value={inputText}
          onChangeText={setInputText}
          multiline
          style={styles.input}
          mode="outlined"
        />
        <Button
          mode="contained"
          onPress={handleSendMessage}
          style={styles.sendButton}
        >
          Send
        </Button>
      </View>
    </View>
  );
}

function ChatMessage({ message }) {
  const isUser = message.role === 'user';
  return (
    <View style={[
      styles.messageBubble,
      isUser ? styles.userMessage : styles.aiMessage
    ]}>
      <Text style={[
        styles.messageText,
        isUser && styles.userMessageText
      ]}>
        {message.content}
      </Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
  messagesList: {
    flex: 1,
  },
  messagesContainer: {
    padding: 12,
  },
  messageBubble: {
    marginVertical: 8,
    marginHorizontal: 12,
    padding: 12,
    borderRadius: 12,
    maxWidth: '85%',
  },
  userMessage: {
    alignSelf: 'flex-end',
    backgroundColor: '#007AFF',
  },
  aiMessage: {
    alignSelf: 'flex-start',
    backgroundColor: '#fff',
    borderWidth: 1,
    borderColor: '#eee',
  },
  messageText: {
    color: '#000',
  },
  userMessageText: {
    color: '#fff',
  },
  inputArea: {
    padding: 12,
    backgroundColor: '#fff',
    borderTopWidth: 1,
    borderTopColor: '#eee',
  },
  input: {
    marginBottom: 8,
  },
  sendButton: {
    paddingVertical: 4,
  },
});
