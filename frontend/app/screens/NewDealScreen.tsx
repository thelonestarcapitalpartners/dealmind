import React from 'react';
import { View, StyleSheet } from 'react-native';
import { Text, Button, SegmentedButtons } from 'react-native-paper';

/**
 * New Deal Screen - Allow users to input deal data via multiple methods
 * 
 * Methods:
 * 1. Paste property URL
 * 2. Upload PDF
 * 3. Upload image
 * 4. Manual entry
 */
export default function NewDealScreen({ navigation }) {
  const [inputMethod, setInputMethod] = React.useState('url');

  const handleCreateDeal = async () => {
    // TODO: Create deal based on input method
    // Call appropriate API endpoint
    navigation.navigate('DealSummary', { dealId: 'new-deal-id' });
  };

  return (
    <View style={styles.container}>
      <Text variant="headlineSmall" style={styles.title}>
        Choose input method
      </Text>

      <SegmentedButtons
        value={inputMethod}
        onValueChange={setInputMethod}
        buttons={[
          { value: 'url', label: 'URL' },
          { value: 'pdf', label: 'PDF' },
          { value: 'image', label: 'Image' },
          { value: 'manual', label: 'Manual' },
        ]}
        style={styles.segmentedButtons}
      />

      {/* TODO: Render input UI based on selected method */}
      <View style={styles.inputArea}>
        <Text variant="bodyMedium">
          Enter details for {inputMethod} input
        </Text>
      </View>

      <Button
        mode="contained"
        onPress={handleCreateDeal}
        style={styles.button}
      >
        Create Deal
      </Button>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 16,
    backgroundColor: '#fff',
  },
  title: {
    marginBottom: 16,
    fontWeight: '600',
  },
  segmentedButtons: {
    marginBottom: 24,
  },
  inputArea: {
    flex: 1,
    borderWidth: 1,
    borderColor: '#ddd',
    borderRadius: 8,
    padding: 16,
    marginBottom: 16,
  },
  button: {
    marginTop: 16,
  },
});
