import React from 'react';
import { View, StyleSheet, ScrollView } from 'react-native';
import { Text, Card, Button, Chip } from 'react-native-paper';

/**
 * Deal Summary Screen - Show key metrics and deal analysis
 * 
 * Displays:
 * - Property photo/info
 * - Deal grade
 * - AI verdict
 * - Key metrics (NOI, Cap Rate, Cash Flow, DSCR, CoC)
 * - Quick action buttons
 */
export default function DealSummaryScreen({ navigation, route }) {
  const { dealId } = route.params;
  const [deal, setDeal] = React.useState(null);

  React.useEffect(() => {
    // TODO: Load deal details from API
  }, [dealId]);

  if (!deal) {
    return (
      <View style={styles.container}>
        <Text>Loading deal...</Text>
      </View>
    );
  }

  return (
    <ScrollView style={styles.container}>
      {/* Deal Grade Badge */}
      <View style={styles.header}>
        <Chip 
          icon="star" 
          style={styles.gradeChip}
        >
          Grade: A
        </Chip>
      </View>

      {/* AI Verdict */}
      <Card style={styles.card}>
        <Card.Content>
          <Text variant="labelSmall">AI Verdict</Text>
          <Text variant="bodyMedium" style={styles.verdict}>
            Strong cash-flow deal at asking price. Verify CapEx and tax assumptions.
          </Text>
        </Card.Content>
      </Card>

      {/* Key Metrics Grid */}
      <View style={styles.metricsGrid}>
        <MetricCard label="Cap Rate" value="6.2%" />
        <MetricCard label="Cash Flow" value="$450/mo" />
        <MetricCard label="CoC Return" value="8.5%" />
        <MetricCard label="DSCR" value="1.28" />
        <MetricCard label="NOI" value="$52k/yr" />
        <MetricCard label="Break-even" value="72%" />
      </View>

      {/* Action Buttons */}
      <Button
        mode="contained"
        onPress={() => navigation.navigate('DealChat', { dealId })}
        style={styles.button}
      >
        Chat with Deal
      </Button>
      <Button
        mode="outlined"
        onPress={() => navigation.navigate('Assumptions', { dealId })}
        style={styles.button}
      >
        Edit Assumptions
      </Button>
    </ScrollView>
  );
}

function MetricCard({ label, value }) {
  return (
    <View style={styles.metricCard}>
      <Text variant="labelSmall" style={styles.metricLabel}>
        {label}
      </Text>
      <Text variant="headlineSmall" style={styles.metricValue}>
        {value}
      </Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 16,
    backgroundColor: '#f5f5f5',
  },
  header: {
    marginBottom: 16,
  },
  gradeChip: {
    alignSelf: 'flex-start',
  },
  card: {
    marginBottom: 16,
  },
  verdict: {
    marginTop: 8,
    fontStyle: 'italic',
  },
  metricsGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: 8,
    marginBottom: 16,
  },
  metricCard: {
    flex: 0.48,
    backgroundColor: '#fff',
    padding: 12,
    borderRadius: 8,
    borderWidth: 1,
    borderColor: '#eee',
  },
  metricLabel: {
    color: '#666',
  },
  metricValue: {
    marginTop: 4,
    fontWeight: '600',
    color: '#2c3e50',
  },
  button: {
    marginVertical: 8,
  },
});
