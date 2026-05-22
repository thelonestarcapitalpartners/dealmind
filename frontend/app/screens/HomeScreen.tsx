import React from 'react';
import { View, StyleSheet } from 'react-native';
import { Text, FAB, ActivityIndicator } from 'react-native-paper';

/**
 * Home Screen - Main dashboard showing recent deals and quick actions
 */
export default function HomeScreen({ navigation }) {
  const [deals, setDeals] = React.useState([]);
  const [loading, setLoading] = React.useState(false);

  React.useEffect(() => {
    // TODO: Load user's deals from API
    setLoading(false);
  }, []);

  return (
    <View style={styles.container}>
      <Text variant="headlineMedium" style={styles.title}>
        Recent Deals
      </Text>
      
      {loading ? (
        <ActivityIndicator animating={true} />
      ) : deals.length === 0 ? (
        <View style={styles.emptyState}>
          <Text variant="bodyLarge">No deals yet</Text>
          <Text variant="bodyMedium" style={styles.emptyText}>
            Create your first deal to get started
          </Text>
        </View>
      ) : (
        // TODO: Render deal list
        <View />
      )}

      <FAB
        icon="plus"
        label="New Deal"
        onPress={() => navigation.navigate('NewDeal')}
        style={styles.fab}
      />
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
  emptyState: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  emptyText: {
    marginTop: 8,
    color: '#666',
  },
  fab: {
    position: 'absolute',
    margin: 16,
    right: 0,
    bottom: 0,
  },
});
