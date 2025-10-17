import { useState } from "react";
import { Bell, Trash2, Send, AlertTriangle, Archive, MoreHorizontal, Search, Filter, RefreshCw } from "lucide-react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";
import { Checkbox } from "@/components/ui/checkbox";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import DashboardHeader from "@/components/DashboardHeader";

interface NotificationItem {
  id: string;
  title: string;
  message: string;
  timestamp: string;
  isRead: boolean;
  priority: "high" | "medium" | "low";
  type: "system" | "alert" | "reminder" | "message";
}

const mockNotifications: NotificationItem[] = [
  {
    id: "1",
    title: "VAT Return Due",
    message: "Your VAT return for Q4 2024 is due in 3 days. Please review and submit.",
    timestamp: "2024-01-15T10:30:00Z",
    isRead: false,
    priority: "high",
    type: "alert"
  },
  {
    id: "2",
    title: "Document Processing Complete",
    message: "Invoice batch INV-2024-001 has been successfully processed and analyzed.",
    timestamp: "2024-01-15T09:15:00Z",
    isRead: true,
    priority: "medium",
    type: "system"
  },
  {
    id: "3",
    title: "Compliance Check Required",
    message: "New tax regulation updates require review of your current compliance status.",
    timestamp: "2024-01-14T16:45:00Z",
    isRead: false,
    priority: "medium",
    type: "reminder"
  }
];

const mockSentNotifications: NotificationItem[] = [
  {
    id: "s1",
    title: "Monthly Report Sent",
    message: "Tax analytics report for December 2024 has been sent to stakeholders.",
    timestamp: "2024-01-10T14:20:00Z",
    isRead: true,
    priority: "low",
    type: "system"
  }
];

const mockSpamNotifications: NotificationItem[] = [
  {
    id: "sp1",
    title: "Suspicious Login Attempt",
    message: "Multiple failed login attempts detected from unknown IP address.",
    timestamp: "2024-01-12T08:30:00Z",
    isRead: false,
    priority: "high",
    type: "alert"
  }
];

const Notifications = () => {
  const [selectedItems, setSelectedItems] = useState<string[]>([]);
  const [searchQuery, setSearchQuery] = useState("");

  const formatTimestamp = (timestamp: string) => {
    const date = new Date(timestamp);
    return date.toLocaleDateString() + " " + date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case "high": return "destructive";
      case "medium": return "secondary";
      case "low": return "outline";
      default: return "outline";
    }
  };

  const getTypeIcon = (type: string) => {
    switch (type) {
      case "alert": return <AlertTriangle className="h-4 w-4" />;
      case "system": return <Bell className="h-4 w-4" />;
      case "reminder": return <Archive className="h-4 w-4" />;
      case "message": return <Send className="h-4 w-4" />;
      default: return <Bell className="h-4 w-4" />;
    }
  };

  const handleSelectItem = (id: string) => {
    setSelectedItems(prev => 
      prev.includes(id) 
        ? prev.filter(item => item !== id)
        : [...prev, id]
    );
  };

  const handleSelectAll = (notifications: NotificationItem[]) => {
    const allIds = notifications.map(n => n.id);
    setSelectedItems(prev => 
      prev.length === allIds.length 
        ? []
        : allIds
    );
  };

  const NotificationList = ({ notifications, showActions = true }: { notifications: NotificationItem[], showActions?: boolean }) => (
    <div className="space-y-3">
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-2">
          <Checkbox 
            checked={selectedItems.length === notifications.length && notifications.length > 0}
            onCheckedChange={() => handleSelectAll(notifications)}
          />
          <span className="text-sm text-muted-foreground">
            {selectedItems.length > 0 ? `${selectedItems.length} selected` : `${notifications.length} notifications`}
          </span>
        </div>
        {showActions && (
          <div className="flex items-center space-x-2">
            <Button variant="ghost" size="sm">
              <RefreshCw className="h-4 w-4 mr-2" />
              Refresh
            </Button>
            <Button variant="ghost" size="sm">
              <Filter className="h-4 w-4 mr-2" />
              Filter
            </Button>
          </div>
        )}
      </div>

      {notifications.length === 0 ? (
        <div className="text-center py-8 text-muted-foreground">
          <Bell className="h-12 w-12 mx-auto mb-4 opacity-50" />
          <p>No notifications found</p>
        </div>
      ) : (
        notifications.map((notification) => (
          <Card key={notification.id} className={`cursor-pointer transition-colors hover:bg-accent/50 ${!notification.isRead ? 'border-l-4 border-l-primary' : ''}`}>
            <CardContent className="p-4">
              <div className="flex items-start space-x-3">
                <Checkbox 
                  checked={selectedItems.includes(notification.id)}
                  onCheckedChange={() => handleSelectItem(notification.id)}
                />
                <div className="flex-1 min-w-0">
                  <div className="flex items-center space-x-2 mb-1">
                    {getTypeIcon(notification.type)}
                    <h3 className={`text-sm font-medium ${!notification.isRead ? 'font-semibold' : ''}`}>
                      {notification.title}
                    </h3>
                    <Badge variant={getPriorityColor(notification.priority)} className="text-xs">
                      {notification.priority}
                    </Badge>
                    {!notification.isRead && (
                      <div className="h-2 w-2 bg-primary rounded-full"></div>
                    )}
                  </div>
                  <p className="text-sm text-muted-foreground mb-2">
                    {notification.message}
                  </p>
                  <p className="text-xs text-muted-foreground">
                    {formatTimestamp(notification.timestamp)}
                  </p>
                </div>
                <DropdownMenu>
                  <DropdownMenuTrigger asChild>
                    <Button variant="ghost" size="icon" className="h-8 w-8">
                      <MoreHorizontal className="h-4 w-4" />
                    </Button>
                  </DropdownMenuTrigger>
                  <DropdownMenuContent align="end">
                    <DropdownMenuItem>Mark as Read</DropdownMenuItem>
                    <DropdownMenuItem>Archive</DropdownMenuItem>
                    <DropdownMenuItem>Move to Spam</DropdownMenuItem>
                    <DropdownMenuItem className="text-destructive">Delete</DropdownMenuItem>
                  </DropdownMenuContent>
                </DropdownMenu>
              </div>
            </CardContent>
          </Card>
        ))
      )}
    </div>
  );

  return (
    <div className="min-h-screen bg-gradient-subtle">
      <DashboardHeader />
      
      <div className="container mx-auto px-6 py-8">
        <div className="mb-8">
          <div className="flex items-center space-x-3 mb-2">
            <div className="h-10 w-10 bg-gradient-primary rounded-lg flex items-center justify-center">
              <Bell className="h-5 w-5 text-primary-foreground" />
            </div>
            <div>
              <h1 className="text-3xl font-bold text-foreground">Notifications</h1>
              <p className="text-muted-foreground">Manage your alerts, messages and system updates</p>
            </div>
          </div>
          
          <div className="flex items-center space-x-4 mt-6">
            <div className="relative flex-1 max-w-md">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-muted-foreground h-4 w-4" />
              <Input 
                placeholder="Search notifications..." 
                className="pl-10"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
              />
            </div>
          </div>
        </div>

        <Card className="bg-card/60 backdrop-blur-xl border-border/50">
          <CardHeader>
            <CardTitle>Notification Center</CardTitle>
            <CardDescription>
              Organize and manage all your notifications in one place
            </CardDescription>
          </CardHeader>
          <CardContent>
            <Tabs defaultValue="inbox" className="w-full">
              <TabsList className="grid w-full grid-cols-4 mb-6">
                <TabsTrigger value="inbox" className="flex items-center space-x-2">
                  <Bell className="h-4 w-4" />
                  <span>Inbox ({mockNotifications.filter(n => !n.isRead).length})</span>
                </TabsTrigger>
                <TabsTrigger value="outbox" className="flex items-center space-x-2">
                  <Send className="h-4 w-4" />
                  <span>Outbox</span>
                </TabsTrigger>
                <TabsTrigger value="spam" className="flex items-center space-x-2">
                  <AlertTriangle className="h-4 w-4" />
                  <span>Spam ({mockSpamNotifications.length})</span>
                </TabsTrigger>
                <TabsTrigger value="trash" className="flex items-center space-x-2">
                  <Trash2 className="h-4 w-4" />
                  <span>Trash</span>
                </TabsTrigger>
              </TabsList>

              <TabsContent value="inbox" className="space-y-4">
                <div className="flex items-center justify-between">
                  <h3 className="text-lg font-semibold">Inbox</h3>
                  <div className="flex items-center space-x-2">
                    <Badge variant="secondary">
                      {mockNotifications.filter(n => !n.isRead).length} unread
                    </Badge>
                  </div>
                </div>
                <NotificationList notifications={mockNotifications} />
              </TabsContent>

              <TabsContent value="outbox" className="space-y-4">
                <div className="flex items-center justify-between">
                  <h3 className="text-lg font-semibold">Sent Notifications</h3>
                  <Badge variant="secondary">{mockSentNotifications.length} sent</Badge>
                </div>
                <NotificationList notifications={mockSentNotifications} />
              </TabsContent>

              <TabsContent value="spam" className="space-y-4">
                <div className="flex items-center justify-between">
                  <h3 className="text-lg font-semibold">Spam</h3>
                  <Badge variant="destructive">{mockSpamNotifications.length} spam</Badge>
                </div>
                <NotificationList notifications={mockSpamNotifications} />
              </TabsContent>

              <TabsContent value="trash" className="space-y-4">
                <div className="flex items-center justify-between">
                  <h3 className="text-lg font-semibold">Trash</h3>
                  <Badge variant="outline">0 deleted</Badge>
                </div>
                <div className="text-center py-8 text-muted-foreground">
                  <Trash2 className="h-12 w-12 mx-auto mb-4 opacity-50" />
                  <p>Trash is empty</p>
                  <p className="text-sm mt-2">Deleted notifications will appear here</p>
                </div>
              </TabsContent>
            </Tabs>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default Notifications;