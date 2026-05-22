import React from 'react';
import { GestureHandlerRootView } from 'react-native-gesture-handler';
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { PaperProvider } from 'react-native-paper';

// Screens
import HomeScreen from './screens/HomeScreen';
import NewDealScreen from './screens/NewDealScreen';
import DealSummaryScreen from './screens/DealSummaryScreen';
import DealChatScreen from './screens/DealChatScreen';
import AssumptionsScreen from './screens/AssumptionsScreen';

const Stack = createNativeStackNavigator();
const Tab = createBottomTabNavigator();

function DealStack() {
  return (
    <Stack.Navigator>
      <Stack.Screen 
        name="DealList" 
        component={HomeScreen}
        options={{ title: 'My Deals' }}
      />
      <Stack.Screen 
        name="NewDeal" 
        component={NewDealScreen}
        options={{ title: 'New Deal' }}
      />
      <Stack.Screen 
        name="DealSummary" 
        component={DealSummaryScreen}
        options={{ title: 'Deal Summary' }}
      />
      <Stack.Screen 
        name="DealChat" 
        component={DealChatScreen}
        options={{ title: 'Chat' }}
      />
      <Stack.Screen 
        name="Assumptions" 
        component={AssumptionsScreen}
        options={{ title: 'Assumptions' }}
      />
    </Stack.Navigator>
  );
}

export default function App() {
  return (
    <GestureHandlerRootView style={{ flex: 1 }}>
      <PaperProvider>
        <NavigationContainer>
          <Tab.Navigator
            screenOptions={{
              headerShown: false,
            }}
          >
            <Tab.Screen 
              name="Deals" 
              component={DealStack}
              options={{
                tabBarLabel: 'Deals',
              }}
            />
            <Tab.Screen 
              name="Profile" 
              component={HomeScreen}
              options={{
                tabBarLabel: 'Profile',
              }}
            />
          </Tab.Navigator>
        </NavigationContainer>
      </PaperProvider>
    </GestureHandlerRootView>
  );
}
